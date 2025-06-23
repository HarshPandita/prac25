import bisect

class CommodityPriceTracker:
    def __init__(self):
        self.timestamp_to_history = {}  # timestamp -> list of (checkpoint, max_price_so_far)
        self.checkpoint = 0             # Global checkpoint counter

    def update(self, timestamp: int, price: int) -> None:
        """
        Add a new price for a given timestamp and create a new checkpoint.
        """
        if timestamp not in self.timestamp_to_history:
            self.timestamp_to_history[timestamp] = []

        history = self.timestamp_to_history[timestamp]

        # Compute new max so far for this timestamp
        prev_max = history[-1][1] if history else float('-inf')
        new_max = max(prev_max, price)

        # Store new max with current checkpoint index
        history.append((self.checkpoint, new_max))
        self.checkpoint += 1

    def query(self, timestamp: int, checkpoint: int) -> int:
        """
        Return the max price for a given timestamp as of the given checkpoint.
        """
        history = self.timestamp_to_history.get(timestamp)
        if not history:
            return None

        # Binary search to find highest checkpoint <= given checkpoint
        lo, hi = 0, len(history) - 1
        result = None

        while lo <= hi:
            mid = (lo + hi) // 2
            cp, price = history[mid]
            if cp <= checkpoint:
                result = price
                lo = mid + 1
            else:
                hi = mid - 1

        return result
