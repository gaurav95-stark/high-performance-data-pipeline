import json
import sqlite3
from pathlib import Path
from threading import Lock
from src.models import EventRecord, utc_now

class EventRepository:
    def __init__(self, database_path):
        self.database_path = database_path
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self._initialize()

    def _connect(self):
        conn = sqlite3.connect(self.database_path, timeout=10)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize(self):
        with self._connect() as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY, event_type TEXT NOT NULL, payload TEXT NOT NULL, status TEXT NOT NULL, received_at TEXT NOT NULL, processed_at TEXT, result TEXT, error TEXT)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_events_status_received ON events(status, received_at)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_events_type_received ON events(event_type, received_at)")

    def create(self, event):
        with self._lock, self._connect() as conn:
            cur = conn.execute("INSERT OR IGNORE INTO events(event_id,event_type,payload,status,received_at) VALUES(?,?,?,?,?)",
                (event.event_id, event.event_type, json.dumps(event.payload), "queued", utc_now()))
            return cur.rowcount == 1

    def update_status(self, event_id, status, result=None, error=None):
        with self._lock, self._connect() as conn:
            conn.execute("UPDATE events SET status=?, processed_at=?, result=?, error=? WHERE event_id=?",
                (status, utc_now() if status in ("processed", "failed") else None,
                 json.dumps(result) if result is not None else None, error, event_id))

    def get(self, event_id):
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM events WHERE event_id=?", (event_id,)).fetchone()
        return self._record(row) if row else None

    def list_recent(self, limit=50):
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM events ORDER BY received_at DESC LIMIT ?", (limit,)).fetchall()
        return [self._record(row) for row in rows]

    @staticmethod
    def _record(row):
        return EventRecord(event_id=row["event_id"], event_type=row["event_type"],
            payload=json.loads(row["payload"]), status=row["status"], received_at=row["received_at"],
            processed_at=row["processed_at"], result=json.loads(row["result"]) if row["result"] else None,
            error=row["error"])
