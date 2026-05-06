#!/usr/bin/env python3
"""Build the site and serve it locally. Kills any existing server, finds a free port."""

from __future__ import annotations

import http.server
import os
import signal
import socket
import socketserver
import subprocess
import sys
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "site"
START_PORT = 8000


def kill_port(port: int) -> None:
    try:
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"], capture_output=True, text=True
        )
        for pid in result.stdout.strip().splitlines():
            os.kill(int(pid), signal.SIGTERM)
    except Exception:
        pass


def find_free_port(start: int) -> int:
    kill_port(start)
    for port in range(start, start + 10):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
                return port
        except OSError:
            continue
    raise RuntimeError("No free port found in range.")


def main() -> int:
    result = subprocess.run([sys.executable, str(ROOT / "tools" / "build.py")])
    if result.returncode != 0:
        return result.returncode

    if not SITE_DIR.exists():
        sys.stderr.write("site/ does not exist after build — aborting.\n")
        return 1

    port = find_free_port(START_PORT)
    os.chdir(SITE_DIR)
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        url = f"http://localhost:{port}"
        print(f"Serving site/ at {url}")
        print("Ctrl-C to stop.")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
