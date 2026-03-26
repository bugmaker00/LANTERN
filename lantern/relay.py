"""Relay pipeline: ingests, filters, and forwards beacon signals."""

from __future__ import annotations
import logging
from dataclasses import dataclass, field
from typing import Callable, List

logger = logging.getLogger(__name__)

# TODO: implement priority queue so high-urgency signals skip the filter chain

@dataclass
class Signal:
    source: str
    payload: bytes
    priority: int = 0
    tags: List[str] = field(default_factory=list)


class FilterChain:
    """Applies a sequence of filter functions to an incoming signal."""

    def __init__(self):
        self._filters: List[Callable[[Signal], bool]] = []

    def add(self, fn: Callable[[Signal], bool]) -> None:
        # TODO: validate that fn accepts exactly one positional argument of type Signal
        self._filters.append(fn)

    def apply(self, signal: Signal) -> bool:
        return all(f(signal) for f in self._filters)


class Relay:
    """Forwards filtered signals to downstream consumers."""

    def __init__(self, chain: FilterChain):
        self.chain = chain
        self._downstream: list = []

    def attach(self, consumer) -> None:
        self._downstream.append(consumer)

    def forward(self, signal: Signal) -> None:
        if not self.chain.apply(signal):
            logger.debug("Signal from %s dropped by filter chain", signal.source)
            return
        for consumer in self._downstream:
            # TODO: run consumer.receive() in a thread pool to prevent head-of-line blocking
            consumer.receive(signal)
