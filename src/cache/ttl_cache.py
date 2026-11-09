import time

class TTLCache:
    def __init__(self, ttl_seconds=30, max_size=2048):
        self.ttl_seconds, self.max_size = ttl_seconds, max_size
        self._items = {}
        self.hits = self.misses = 0

    def get(self, key):
        item = self._items.get(key)
        if item is None:
            self.misses += 1
            return None
        expiry, value = item
        if expiry <= time.monotonic():
            self._items.pop(key, None)
            self.misses += 1
            return None
        self.hits += 1
        return value

    def set(self, key, value):
        if key not in self._items and len(self._items) >= self.max_size:
            oldest = min(self._items, key=lambda k: self._items[k][0])
            self._items.pop(oldest, None)
        self._items[key] = (time.monotonic() + self.ttl_seconds, value)

    def clear(self):
        self._items.clear()

    @property
    def hit_ratio(self):
        total = self.hits + self.misses
        return self.hits / total if total else 0.0
