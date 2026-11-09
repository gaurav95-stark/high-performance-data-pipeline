from src.services.observers import EventObserver

def test_observer():
    seen = []
    observer = EventObserver()
    observer.subscribe(lambda name, data: seen.append((name, data)))
    observer.notify("accepted", {"id":"a"})
    assert seen == [("accepted", {"id":"a"})]
