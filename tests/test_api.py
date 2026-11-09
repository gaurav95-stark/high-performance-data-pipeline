def test_api_smoke(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "api.db"))
    import importlib, src.config, src.api.main
    importlib.reload(src.config)
    module = importlib.reload(src.api.main)
    from fastapi.testclient import TestClient
    with TestClient(module.app) as client:
        assert client.get("/health").status_code == 200
        r = client.post("/events", json={"event_id":"a1","event_type":"view","payload":{"page":"/"}})
        assert r.status_code == 202 and r.json()["accepted"]
        assert client.get("/events/a1").status_code == 200
        assert client.get("/events").status_code == 200
        assert client.get("/cache/stats").status_code == 200
        assert client.get("/metrics").status_code == 200
