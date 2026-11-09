import pytest
from src.services.strategies import StrategyFactory, NormalizeStrategy, EnrichStrategy

@pytest.mark.asyncio
async def test_normalize():
    out = await NormalizeStrategy().process({"event_type":"x","payload":{" User_ID ":1}})
    assert out["normalized_payload"] == {"user_id":1}

@pytest.mark.asyncio
async def test_enrich():
    out = await EnrichStrategy().process({"event_type":"x","payload":{"user_id":1}})
    assert out["field_count"] == 1 and out["has_user_id"]

def test_factory():
    assert isinstance(StrategyFactory.create("normalize"), NormalizeStrategy)
    assert isinstance(StrategyFactory.create("enrich"), EnrichStrategy)
    with pytest.raises(ValueError):
        StrategyFactory.create("bad")
