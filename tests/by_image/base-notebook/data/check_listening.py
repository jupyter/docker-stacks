#!/usr/bin/env python
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import socket
import time

import requests


def make_get_request() -> None:
    # Give some time for server to start
    finish_time = time.time() + 10
    sleep_time = 1
    while time.time() < finish_time:
        time.sleep(sleep_time)
        try:
            resp = requests.get("http://localhost:8888/api")
            resp.raise_for_status()
        except requests.RequestException:
            pass
    resp.raise_for_status()


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
