import time
from collections import defaultdict, deque


class RateLimiter:
    """Tiny in-memory sliding window (per client key). Prototype-level abuse protection only."""
    def __init__(self, limit=40, window=60):
        self.limit, self.window, self.hits = limit, window, defaultdict(deque)

    def allow(self, key, now=None):
        now = time.monotonic() if now is None else now
        q = self.hits[key]
        while q and now - q[0] > self.window:
            q.popleft()
        if len(q) >= self.limit:
            return False
        q.append(now)
        return True
