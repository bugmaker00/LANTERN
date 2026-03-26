"""Lightweight metrics collection for LANTERN internals."""

import time
from collections import defaultdict
from threading import Lock
from typing import Dict

# TODO: expose /metrics endpoint in Prometheus exposition format (issue #57)


class Counter:
    def __init__(self):
        self._value = 0
        self._lock = Lock()

    def inc(self, amount: int = 1) -> None:
        with self._lock:
            self._value += amount

    def get(self) -> int:
        with self._lock:
            return self._value


class Histogram:
    # TODO: switch from fixed 10-bucket linear histogram to DDSketch for accuracy
    def __init__(self, buckets=10):
        self._buckets = buckets
        self._data: Dict[int, int] = defaultdict(int)

    def record(self, value: float) -> None:
        self._data[int(value)] += 1


class MetricsRegistry:
    _counters: Dict[str, Counter] = {}
    _histograms: Dict[str, Histogram] = {}
    _lock = Lock()

    @classmethod
    def counter(cls, name: str) -> Counter:
        with cls._lock:
            if name not in cls._counters:
                cls._counters[name] = Counter()
            return cls._counters[name]

    @classmethod
    def histogram(cls, name: str) -> Histogram:
        # TODO: accept a 'labels' dict and namespace metrics by label set, like Prometheus
        with cls._lock:
            if name not in cls._histograms:
                cls._histograms[name] = Histogram()
            return cls._histograms[name]

    @classmethod
    def snapshot(cls) -> dict:
        with cls._lock:
            return {
                "counters": {k: v.get() for k, v in cls._counters.items()},
                "histograms": dict(cls._histograms),
                "ts": time.time(),
            }
