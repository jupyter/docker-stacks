# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging
import time
from typing import Optional

import pytest  # type: ignore

from tests.conftest import TrackedContainer, get_health

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "env",
    [
        None,
        ["DOCKER_STACKS_JUPYTER_CMD=lab"],
        ["RESTARTABLE=yes"],
        ["DOCKER_STACKS_JUPYTER_CMD=notebook"],
        ["DOCKER_STACKS_JUPYTER_CMD=server"],
        ["DOCKER_STACKS_JUPYTER_CMD=nbclassic"],
    ],
)
def test_health(container: TrackedContainer, env: Optional[list[str]]) -> None:
    running_container = container.run_detached(
        tty=True,
        environment=env,
    )
    # sleeping some time to let the server start
    time.sleep(15)
    assert get_health(running_container) == "healthy"
