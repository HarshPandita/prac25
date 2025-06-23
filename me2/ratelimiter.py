import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests: int, window_size: int):
        self.max_requests = max_requests
        self.window_size = window_size
        self.user_data = defaultdict(lambda: {
            "window_start": 0,
            "requests_used": 0,
            "carryover": 0
        })

    def is_allowed(self, user_id: str) -> bool:
        current_time = int(time.time())
        window_start = current_time - (current_time % self.window_size)

        data = self.user_data[user_id]

        # First request: initialize window
        if data["window_start"] == 0:
            data["window_start"] = window_start

        # New window: reset usage and update carryover
        elif data["window_start"] != window_start:
            unused = max(0, self.max_requests - data["requests_used"])
            data["carryover"] = min(self.max_requests, data["carryover"] + unused)
            data["requests_used"] = 0
            data["window_start"] = window_start

        allowed_limit = self.max_requests + data["carryover"]

        if data["requests_used"] < allowed_limit:
            data["requests_used"] += 1
            return True
        else:
            return False


limiter = RateLimiter(max_requests=5, window_size=60)

user = "user123"
for i in range(7):
    print(f"Request {i+1}: {limiter.is_allowed(user)}")
    time.sleep(0.5)


# 
        
import time
# o(1)
class TokenBucket:
    def __init__(self, capacity, refill_rate_per_sec):
        self.capacity = capacity                      # Max tokens that can be held
        self.tokens = capacity                        # Start full
        self.refill_rate = refill_rate_per_sec        # Tokens added per second
        self.last_refill_time = time.time()           # Timestamp of last token update

    def allow_request(self):
        current_time = time.time()
        elapsed = current_time - self.last_refill_time
        refill = elapsed * self.refill_rate           # How many tokens should be added since last check

        self.tokens = min(self.capacity, self.tokens + refill)  # Add tokens (cap at capacity)
        self.last_refill_time = current_time          # Update the refill time

        if self.tokens >= 1:
            self.tokens -= 1                          # Consume a token
            return True
        return False                                   # Not enough tokens → deny request

