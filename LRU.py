from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()   # key → value

    def _mark_as_recent(self, key: int) -> None:
        value = self.cache.pop(key)
        self.cache[key] = value

    def _evict_lru(self) -> None:
        for oldest_key in self.cache:
            # This is the first inserted (LRU) key in OrderedDict
            del self.cache[oldest_key]
            break

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self._mark_as_recent(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Remove so we can reinsert at the end
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            self._evict_lru()
        self.cache[key] = value
