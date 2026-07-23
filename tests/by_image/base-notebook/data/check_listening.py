#!/usr/bin/env python
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import socket
import time

import requests


def make_get_request() -> None:
    """Wait for the server to start answering GET requests."""
    deadline = time.monotonic() + 30
    last_error: requests.RequestException | None = None
    while time.monotonic() < deadline:
        try:
            resp = requests.get("http://localhost:8888/api", timeout=10)
            resp.raise_for_status()
            return
        except requests.RequestException as e:
            last_error = e
            time.sleep(1)
    if last_error is not None:
        raise last_error
    raise RuntimeError("Server did not respond within the deadline")


def check_addrs(family: socket.AddressFamily) -> None:
    assert family in {socket.AF_INET, socket.AF_INET6}

    # https://docs.python.org/3/library/socket.html#socket.getaddrinfo
    addrs = {
        s[4][0]
        for s in socket.getaddrinfo(host=socket.gethostname(), port=None, family=family)
    }
    loopback_addr = "127.0.0.1" if family == socket.AF_INET else "::1"
    addrs.discard(loopback_addr)

    assert addrs, f"No external addresses found for family: {family}"

    for addr in addrs:
        url = (
            f"http://{addr}:8888/api"
            if family == socket.AF_INET
            else f"http://[{addr}]:8888/api"
        )
        r = requests.get(url)
        r.raise_for_status()
        assert "version" in r.json()
        print(f"Successfully connected to: {url}")


def test_connect() -> None:
    make_get_request()

    check_addrs(socket.AF_INET)
    check_addrs(socket.AF_INET6)


if __name__ == "__main__":
    test_connect()
