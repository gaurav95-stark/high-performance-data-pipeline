import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from prometheus_client import make_asgi_app
from src.config import settings
from src.models import EventIn
from src.database.repository import EventRepository
from src.cache.ttl_cache import TTLCache
from src.services.observers import EventObserver
from src.services.strategies import StrategyFactory
from src.services.pipeline import DataPipeline
from src.services.metrics import EVENTS_ACCEPTED

logging.basicConfig(level=settings.log_level)
repository = EventRepository(settings.database_path)
cache = TTLCache(settings.cache_ttl_seconds)
observer = EventObserver()
observer.subscribe(lambda name, data: logging.getLogger("pipeline.events").info("%s %s", name, data))
pipeline = DataPipeline(repository, StrategyFactory.create("enrich"), observer,
                        settings.worker_count, settings.queue_max_size)

@asynccontextmanager
async def lifespan(app):
    await pipeline.start()
    yield
    await pipeline.stop()

app = FastAPI(title="Real-Time Data Processing Pipeline", version="1.0.0", lifespan=lifespan)
app.mount("/metrics", make_asgi_app())

@app.get("/health")
async def health():
    return {"status": "ok", "queue_depth": pipeline.queue.qsize(), "workers": pipeline.worker_count}

@app.post("/events", status_code=202)
async def ingest_event(event: EventIn):
    try:
        accepted = await pipeline.submit(event)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Pipeline unavailable: {exc}")
    if not accepted:
        return {"accepted": False, "duplicate": True, "event": repository.get(event.event_id)}
    EVENTS_ACCEPTED.inc()
    cache.clear()
    return {"accepted": True, "event_id": event.event_id, "status": "queued"}

@app.get("/events/{event_id}")
async def get_event(event_id: str):
    cached = cache.get(event_id)
    if cached is not None:
        return cached
    record = repository.get(event_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Event not found")
    data = record.model_dump()
    cache.set(event_id, data)
    return data

@app.get("/events")
async def list_events(limit: int = Query(default=50, ge=1, le=500)):
    return [item.model_dump() for item in repository.list_recent(limit)]

@app.get("/cache/stats")
async def cache_stats():
    return {"hits": cache.hits, "misses": cache.misses, "hit_ratio": cache.hit_ratio}
