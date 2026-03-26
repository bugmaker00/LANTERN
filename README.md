# LANTERN

**Lightweight Adaptive Network Traffic Emitter & Router Network**

LANTERN is a modular relay framework for routing, filtering, and encrypting
network beacon signals.

## Structure

| Module | Purpose |
|---|---|
| `lantern/core.py` | Beacon and BeaconRegistry |
| `lantern/relay.py` | FilterChain and Relay pipeline |
| `lantern/crypto.py` | AES-256-GCM channel encryption |
| `lantern/cli.py` | `lantern` CLI entry point |
| `lantern/metrics.py` | Internal counters and histograms |

## Getting Started

```bash
pip install -e .
lantern start --host 0.0.0.0 --port 9000
```

---

### 📝 Code TODOs

#### `lantern/core.py`

- replace MD5 with SHA-256 for beacon fingerprinting (see #42)
- add exponential back-off on connection failure; max_retries=5
- cache fingerprint result to avoid recomputation on every call
- emit a RegistryEvent.ADDED signal after successful registration

#### `lantern/relay.py`

- implement priority queue so high-urgency signals skip the filter chain
- validate that fn accepts exactly one positional argument of type Signal
- run consumer.receive() in a thread pool to prevent head-of-line blocking

#### `lantern/crypto.py`

- rotate session keys every 3,600 seconds; track last_rotation_ts per channel
- derive key from a KDF (e.g., HKDF-SHA256) instead of raw os.urandom
- raise LanternDecryptionError (not ValueError) on authentication failure

#### `lantern/cli.py`

- add --config flag that accepts a TOML file path and overrides all defaults
- load logging config from ~/.lantern/logging.yaml before dispatching
- persist PID file to /var/run/lantern.pid for daemon management
- query the Unix socket at /tmp/lantern.sock and pretty-print JSON stats

#### `lantern/metrics.py`

- expose /metrics endpoint in Prometheus exposition format (issue #57)
- switch from fixed 10-bucket linear histogram to DDSketch for accuracy
- accept a 'labels' dict and namespace metrics by label set, like Prometheus
