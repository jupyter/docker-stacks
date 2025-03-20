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


def test_connect() -> None:
    make_get_request()

    # https://docs.python.org/3/library/socket.html#socket.getaddrinfo
    ipv4_addrs = {
        s[4][0] for s in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET)
    }
    ipv4_addrs.discard("127.0.0.1")
    if len(ipv4_addrs) < 1:
        raise Exception("No external IPv4 addresses found")
    for addr in ipv4_addrs:
        url = f"http://{addr}:8888/api"
        r = requests.get(url)
        r.raise_for_status()
        assert "version" in r.json()
        print(f"Successfully connected to IPv4 {url}")

    ipv6_addrs = {
        s[4][0] for s in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)
    }
    ipv6_addrs.discard("::1")
    if len(ipv6_addrs) < 1:
        raise Exception("No external IPv6 addresses found")
    for addr in ipv6_addrs:
        url = f"http://[{addr}]:8888/api"
        r = requests.get(url)
        r.raise_for_status()
        assert "version" in r.json()
        print(f"Successfully connected to IPv6 {url}")


if __name__ == "__main__":
    test_connect()
