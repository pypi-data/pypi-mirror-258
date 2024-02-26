from collections import deque
import typing as t


T = t.TypeVar('T')


class Qbuffer(t.Generic[T]):
    def __init__(
        self,
        *,
        size: int,
        callback: t.Callable[[T], None],
        flush_callback: t.Callable[[], None] = lambda: None,
    ):
        self.size = size
        self.callback = callback
        self.flush_callback = flush_callback
        self.queue: deque[T] = deque()

    def append(self, item: T, *, flush=False):
        self.queue.append(item)
        if len(self.queue) >= self.size:
            self.flush()
        if flush:
            self.flush()

    def extend(self, items: t.Iterable[T], *, flush=False):
        for item in items:
            self.append(item)
        if flush:
            self.flush()

    def __del__(self):
        self.close()

    def close(self):
        self.flush()

    def flush(self):
        while self.queue:
            self.callback(self.queue.popleft())
        self.flush_callback()
