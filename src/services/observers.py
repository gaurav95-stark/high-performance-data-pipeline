class EventObserver:
    def __init__(self):
        self._listeners = []

    def subscribe(self, listener):
        self._listeners.append(listener)

    def notify(self, event_name, data):
        for listener in tuple(self._listeners):
            listener(event_name, data)
