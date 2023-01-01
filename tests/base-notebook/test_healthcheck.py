# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging
import time

from tests.conftest import TrackedContainer, get_health

LOGGER = logging.getLogger(__name__)


def test_health(container: TrackedContainer) -> None:
    running_container = container.run_detached(
        tty=True,
    )
    # sleeping some time to let the server start
    time.sleep(15)
    assert get_health(running_container) == "healthy"
