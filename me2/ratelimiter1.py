import time
import threading
from collections import defaultdict

class UserBucket:
    def __init__(self, max_tokens, refill_interval, max_credits=None):
        self.capacity = max_tokens
        self.tokens = max_tokens
        self.credits = 0
        self.max_credits = max_credits or max_tokens
        self.refill_interval = refill_interval
        self.last_refill_time = time.time()
        # self.lock = threading.Lock()  # 🔐 Add a lock per user

    def refill(self):
        current_time = time.time()
        elapsed = current_time - self.last_refill_time

        if elapsed >= self.refill_interval:
            unused = self.capacity - self.tokens
            self.credits = min(self.credits + unused, self.max_credits)
            self.tokens = self.capacity
            self.last_refill_time = current_time

    def allow_request(self):
        # with self.lock:  # 🔒 Protect the entire request flow
            self.refill()

            if self.tokens > 0:
                self.tokens -= 1
                return True
            elif self.credits > 0:
                self.credits -= 1
                return True
            else:
                return False


class RateLimiter:
    def __init__(self, max_requests, window_seconds, max_credit_cap=None):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.max_credit_cap = max_credit_cap or max_requests
        self.user_buckets = {}
        # self.registry_lock = threading.Lock()  # 🔐 Lock to protect user bucket creation

    def get_bucket(self, user_id):
        if user_id not in self.user_buckets:
            # with self.registry_lock:
                # if user_id not in self.user_buckets:
            self.user_buckets[user_id] = UserBucket(
                self.max_requests, self.window_seconds, self.max_credit_cap
            )
        return self.user_buckets[user_id]

    def is_allowed(self, user_id):
        # print(self.get_bucket(user_id).allow_request())
        return self.get_bucket(user_id).allow_request()
    

limiter = RateLimiter(max_requests=3, window_seconds=5)
user = "user1"

print(limiter.is_allowed(user))  # 1st request
time.sleep(1)
print(limiter.is_allowed(user))
time.sleep(1)
print(limiter.is_allowed(user))
time.sleep(1)
print(limiter.is_allowed(user))
time.sleep(1)

print(limiter.is_allowed(user))  # 1st request
time.sleep(1)
print(limiter.is_allowed(user))
time.sleep(1)
print(limiter.is_allowed(user))
time.sleep(1)
print(limiter.is_allowed(user))
