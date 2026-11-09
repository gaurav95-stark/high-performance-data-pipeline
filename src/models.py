from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, Field

class EventIn(BaseModel):
    event_id: str = Field(min_length=1, max_length=128)
    event_type: str = Field(min_length=1, max_length=80)
    payload: dict[str, Any]

class EventRecord(BaseModel):
    event_id: str
    event_type: str
    payload: dict[str, Any]
    status: str
    received_at: str
    processed_at: str | None = None
    result: dict[str, Any] | None = None
    error: str | None = None

def utc_now():
    return datetime.now(timezone.utc).isoformat()
