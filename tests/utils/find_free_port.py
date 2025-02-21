# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import socket
from contextlib import closing


def find_free_port() -> str:
    """Returns the available host port. Can be called in multiple threads/processes."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]  # type: ignore
