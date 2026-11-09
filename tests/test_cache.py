from src.cache.ttl_cache import TTLCache

def test_cache_hit_miss_and_ratio():
    c = TTLCache()
    assert c.get("nope") is None
    c.set("a", 1)
    assert c.get("a") == 1
    assert c.hits == 1 and c.misses == 1 and c.hit_ratio == .5

def test_cache_capacity_and_clear():
    c = TTLCache(max_size=1)
    c.set("a", 1); c.set("b", 2)
    assert c.get("a") is None and c.get("b") == 2
    c.clear()
    assert c.get("b") is None
