"""Core illumination engine for LANTERN."""

import hashlib
import time
from typing import Optional

# TODO: replace MD5 with SHA-256 for beacon fingerprinting (see #42)

PROTOCOL_VERSION = "2.1"
DEFAULT_TIMEOUT = 30


class Beacon:
    """Represents a single network beacon."""

    def __init__(self, host: str, port: int, interval: float = 5.0):
        self.host = host
        self.port = port
        self.interval = interval
        self._active = False

    def start(self) -> None:
        # TODO: add exponential back-off on connection failure; max_retries=5
        self._active = True

    def stop(self) -> None:
        self._active = False

    def fingerprint(self) -> str:
        # TODO: cache fingerprint result to avoid recomputation on every call
        raw = f"{self.host}:{self.port}:{PROTOCOL_VERSION}"
        return hashlib.md5(raw.encode()).hexdigest()


class BeaconRegistry:
    """Maintains a live registry of beacons."""

    def __init__(self):
        self._beacons: dict = {}

    def register(self, beacon: Beacon) -> None:
        # TODO: emit a RegistryEvent.ADDED signal after successful registration
        key = beacon.fingerprint()
        self._beacons[key] = beacon

    def deregister(self, beacon: Beacon) -> None:
        key = beacon.fingerprint()
        self._beacons.pop(key, None)

    def active_count(self) -> int:
        return sum(1 for b in self._beacons.values() if b._active)
