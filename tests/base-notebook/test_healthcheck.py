# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging
import time
from typing import Optional

import pytest  # type: ignore

from tests.conftest import TrackedContainer, get_health

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "env,cmd",
    [
        (None, None),
        (["DOCKER_STACKS_JUPYTER_CMD=lab"], None),
        (["DOCKER_STACKS_JUPYTER_CMD=notebook"], None),
        (["DOCKER_STACKS_JUPYTER_CMD=server"], None),
        (["DOCKER_STACKS_JUPYTER_CMD=nbclassic"], None),
        (["RESTARTABLE=yes"], None),
        (["JUPYTER_PORT=8171"], None),
        (["JUPYTER_PORT=8117", "DOCKER_STACKS_JUPYTER_CMD=notebook"], None),
        (None, ["start-notebook.sh", "--NotebookApp.base_url=/test"]),
        (None, ["start-notebook.sh", "--NotebookApp.base_url=/test/"]),
        (["GEN_CERT=1"], ["start-notebook.sh", "--NotebookApp.base_url=/test"]),
        (
            ["GEN_CERT=1", "JUPYTER_PORT=7891"],
            ["start-notebook.sh", "--NotebookApp.base_url=/test"],
        ),
        (["NB_USER=testuser", "CHOWN_HOME=1"], None),
        (["NB_USER='test user'", "CHOWN_HOME=1"], None),
        (
            ["NB_USER=testuser", "CHOWN_HOME=1"],
            ["start-notebook.sh", "--NotebookApp.base_url=/test"],
        ),
        (
            ["NB_USER='test user'", "CHOWN_HOME=1"],
            ["start-notebook.sh", "--NotebookApp.base_url=/test"],
        ),
        (
            ["NB_USER=testuser", "CHOWN_HOME=1", "JUPYTER_PORT=8123"],
            ["start-notebook.sh", "--NotebookApp.base_url=/test"],
        ),
    ],
)
def test_health(
    container: TrackedContainer,
    env: Optional[list[str]],
    cmd: Optional[list[str]],
) -> None:
    running_container = container.run_detached(
        tty=True,
        environment=env,
        command=cmd,
    )

    # sleeping some time to let the server start
    time_spent = 0.0
    wait_time = 0.1
    time_limit = 15
    while time_spent < time_limit:
        time.sleep(wait_time)
        time_spent += wait_time
        if get_health(running_container) == "healthy":
            return

    assert get_health(running_container) == "healthy"
