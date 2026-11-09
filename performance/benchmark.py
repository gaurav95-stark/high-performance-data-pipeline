import asyncio, tempfile, time
from pathlib import Path
from src.database.repository import EventRepository
from src.models import EventIn
from src.services.observers import EventObserver
from src.services.pipeline import DataPipeline
from src.services.strategies import StrategyFactory

async def run_benchmark(count=500, workers=4):
    with tempfile.TemporaryDirectory() as folder:
        repo = EventRepository(str(Path(folder) / "bench.db"))
        pipe = DataPipeline(repo, StrategyFactory.create("enrich"), EventObserver(),
                            workers, queue_max_size=count + 1)
        await pipe.start()
        start = time.perf_counter()
        try:
            for i in range(count):
                await pipe.submit(EventIn(event_id=f"bench-{i}", event_type="bench",
                                          payload={"user_id":i, "value":i*2}))
            await asyncio.wait_for(pipe.queue.join(), 60)
            elapsed = time.perf_counter() - start
        finally:
            await pipe.stop()
        print(f"events={count} workers={workers} elapsed_s={elapsed:.4f} throughput_eps={count/elapsed:.2f}")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
