import asyncio
import pytest
from src.database.repository import EventRepository
from src.models import EventIn
from src.services.observers import EventObserver
from src.services.strategies import StrategyFactory
from src.services.pipeline import DataPipeline

@pytest.mark.asyncio
async def test_pipeline_processes_and_deduplicates(tmp_path):
    repo = EventRepository(str(tmp_path / "pipe.db"))
    pipe = DataPipeline(repo, StrategyFactory.create("enrich"), EventObserver(), 2)
    await pipe.start()
    try:
        event = EventIn(event_id="p1", event_type="click", payload={"user_id":1})
        assert await pipe.submit(event)
        await asyncio.wait_for(pipe.queue.join(), 3)
        assert repo.get("p1").status == "processed"
        assert repo.get("p1").result["has_user_id"]
        assert not await pipe.submit(event)
    finally:
        await pipe.stop()
