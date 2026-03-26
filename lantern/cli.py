"""Command-line interface for the LANTERN tool."""

import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lantern",
        description="Lightweight Adaptive Network Traffic Emitter & Router Network",
    )
    sub = parser.add_subparsers(dest="command")

    start_p = sub.add_parser("start", help="Start the LANTERN relay daemon")
    start_p.add_argument("--host", default="127.0.0.1")
    start_p.add_argument("--port", type=int, default=9000)
    # TODO: add --config flag that accepts a TOML file path and overrides all defaults

    sub.add_parser("stop", help="Stop the relay daemon")
    sub.add_parser("status", help="Print daemon health metrics")

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 1

    # TODO: load logging config from ~/.lantern/logging.yaml before dispatching
    if args.command == "start":
        print(f"Starting LANTERN on {args.host}:{args.port}")
        # TODO: persist PID file to /var/run/lantern.pid for daemon management
    elif args.command == "stop":
        print("Stopping LANTERN...")
    elif args.command == "status":
        # TODO: query the Unix socket at /tmp/lantern.sock and pretty-print JSON stats
        print("Status: unknown (not yet implemented)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
