import heapq
# Method	Time Complexity	Explanation
# update()	O(logn)	                Push into both heaps
# current()	O(1)	                Return value from hash map
# maximum()	O(logn) (worst case)	Lazy pop invalid entries from max heap
# minimum()	O(logn) (worst case)	Lazy pop invalid entries from min heap
# Space	O(n)	                    Storing n timestamps in map and heaps

class StockPrice:

    def __init__(self):
        self.timestamp_to_price = {}       # Map timestamp -> price
        self.max_heap = []                 # Max heap of (-price, timestamp)
        self.min_heap = []                 # Min heap of (price, timestamp)
        self.latest_timestamp = -1         # Track latest timestamp

    def update(self, timestamp: int, price: int) -> None:
        self.timestamp_to_price[timestamp] = price
        self.latest_timestamp = max(self.latest_timestamp, timestamp)

        # Push new entry to both heaps
        heapq.heappush(self.max_heap, (-price, timestamp))
        heapq.heappush(self.min_heap, (price, timestamp))

    def current(self) -> int:
        return self.timestamp_to_price[self.latest_timestamp]

    def maximum(self) -> int:
        # Lazy removal of outdated max values
        while True:
            price, timestamp = self.max_heap[0]
            if self.timestamp_to_price[timestamp] == -price:
                return -price
            heapq.heappop(self.max_heap)  # Discard stale entry

    def minimum(self) -> int:
        # Lazy removal of outdated min values
        while True:
            price, timestamp = self.min_heap[0]
            if self.timestamp_to_price[timestamp] == price:
                return price
            heapq.heappop(self.min_heap)  # Discard stale entry
