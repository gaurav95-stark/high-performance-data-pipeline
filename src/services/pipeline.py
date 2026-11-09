import asyncio
import logging
import time
from src.services.metrics import EVENTS_PROCESSED, EVENTS_FAILED, PROCESSING_SECONDS, QUEUE_DEPTH, ACTIVE_WORKERS

logger = logging.getLogger(__name__)

class DataPipeline:
    def __init__(self, repository, strategy, observer, worker_count=4, queue_max_size=1000):
        self.repository, self.strategy, self.observer = repository, strategy, observer
        self.queue = asyncio.Queue(maxsize=queue_max_size)
        self.worker_count = worker_count
        self._tasks = []
        self._running = False

    async def start(self):
        if self._running:
            return
        self._running = True
        ACTIVE_WORKERS.set(self.worker_count)
        self._tasks = [asyncio.create_task(self._worker()) for _ in range(self.worker_count)]

    async def stop(self):
        if not self._running:
            return
        self._running = False
        for _ in self._tasks:
            await self.queue.put(None)
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()

    async def submit(self, event):
        if not self.repository.create(event):
            return False
        await self.queue.put(event.model_dump())
        QUEUE_DEPTH.set(self.queue.qsize())
        self.observer.notify("accepted", {"event_id": event.event_id})
        return True

    async def _worker(self):
        while True:
            item = await self.queue.get()
            QUEUE_DEPTH.set(self.queue.qsize())
            try:
                if item is None:
                    return
                started = time.perf_counter()
                try:
                    result = await self.strategy.process(item)
                    self.repository.update_status(item["event_id"], "processed", result=result)
                    EVENTS_PROCESSED.inc()
                    self.observer.notify("processed", {"event_id": item["event_id"]})
                except Exception as exc:
                    self.repository.update_status(item["event_id"], "failed", error=str(exc))
                    EVENTS_FAILED.inc()
                    logger.exception("Processing failed for %s", item.get("event_id"))
                finally:
                    PROCESSING_SECONDS.observe(time.perf_counter() - started)
            finally:
                self.queue.task_done()
