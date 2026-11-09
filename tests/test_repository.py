from src.database.repository import EventRepository
from src.models import EventIn

def test_repository_crud_and_duplicate(tmp_path):
    repo = EventRepository(str(tmp_path / "test.db"))
    event = EventIn(event_id="e1", event_type="click", payload={"x":1})
    assert repo.create(event)
    assert not repo.create(event)
    assert repo.get("e1").status == "queued"
    repo.update_status("e1", "processed", result={"ok":True})
    assert repo.get("e1").result == {"ok":True}
    assert len(repo.list_recent(10)) == 1
    assert repo.get("absent") is None
