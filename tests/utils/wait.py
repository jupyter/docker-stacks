# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import time
from collections.abc import Callable


def wait_until(
    predicate: Callable[[], bool],
    *,
    timeout: float = 10.0,
    interval: float = 1.0,
) -> bool:
    """Call ``predicate`` until it returns True or ``timeout`` elapses.

    Useful when something becomes ready asynchronously (a container's buffered
    logs, a health status, a booting server). Returns whether it succeeded.
    """
    finish_time = time.monotonic() + timeout
    while time.monotonic() < finish_time:
        if predicate():
            return True
        time.sleep(interval)
    return False
