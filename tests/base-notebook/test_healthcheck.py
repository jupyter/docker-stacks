# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
import time
from typing import Optional

import pytest  # type: ignore

from tests.conftest import TrackedContainer, get_health

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "env,cmd,user",
    [
        (None, None, None),
        (["DOCKER_STACKS_JUPYTER_CMD=lab"], None, None),
        (["DOCKER_STACKS_JUPYTER_CMD=notebook"], None, None),
        (["DOCKER_STACKS_JUPYTER_CMD=server"], None, None),
        (["DOCKER_STACKS_JUPYTER_CMD=nbclassic"], None, None),
        (["RESTARTABLE=yes"], None, None),
        (["JUPYTER_PORT=8171"], None, None),
        (["JUPYTER_PORT=8117", "DOCKER_STACKS_JUPYTER_CMD=notebook"], None, None),
        (None, ["start-notebook.sh"], None),
        (None, ["start-notebook.py", "--ServerApp.base_url=/test"], None),
        (None, ["start-notebook.py", "--ServerApp.base_url=/test/"], None),
        (["GEN_CERT=1"], ["start-notebook.py", "--ServerApp.base_url=/test"], None),
        (
            ["GEN_CERT=1", "JUPYTER_PORT=7891"],
            ["start-notebook.py", "--ServerApp.base_url=/test"],
            None,
        ),
        (["NB_USER=testuser", "CHOWN_HOME=1"], None, "root"),
        (
            ["NB_USER=testuser", "CHOWN_HOME=1"],
            ["start-notebook.py", "--ServerApp.base_url=/test"],
            "root",
        ),
        (
            ["NB_USER=testuser", "CHOWN_HOME=1", "JUPYTER_PORT=8123"],
            ["start-notebook.py", "--ServerApp.base_url=/test"],
            "root",
        ),
    ],
)
def test_health(
    container: TrackedContainer,
    env: Optional[list[str]],
    cmd: Optional[list[str]],
    user: Optional[str],
) -> None:
    running_container = container.run_detached(
        tty=True,
        environment=env,
        command=cmd,
        user=user,
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


@pytest.mark.parametrize(
    "env,cmd,user",
    [
        (
            ["HTTPS_PROXY=host.docker.internal", "HTTP_PROXY=host.docker.internal"],
            None,
            None,
        ),
        (
            [
                "NB_USER=testuser",
                "CHOWN_HOME=1",
                "JUPYTER_PORT=8123",
                "HTTPS_PROXY=host.docker.internal",
                "HTTP_PROXY=host.docker.internal",
            ],
            ["start-notebook.py", "--ServerApp.base_url=/test"],
            "root",
        ),
    ],
)
def test_health_proxy(
    container: TrackedContainer,
    env: Optional[list[str]],
    cmd: Optional[list[str]],
    user: Optional[str],
) -> None:
    running_container = container.run_detached(
        tty=True,
        environment=env,
        command=cmd,
        user=user,
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


@pytest.mark.parametrize(
    "env,cmd,user",
    [
        (["NB_USER=testuser", "CHOWN_HOME=1"], None, None),
        (
            ["NB_USER=testuser", "CHOWN_HOME=1"],
            ["start-notebook.py", "--ServerApp.base_url=/test"],
            None,
        ),
        (
            ["NB_USER=testuser", "CHOWN_HOME=1", "JUPYTER_PORT=8123"],
            ["start-notebook.py", "--ServerApp.base_url=/test"],
            None,
        ),
    ],
)
def test_not_healthy(
    container: TrackedContainer,
    env: Optional[list[str]],
    cmd: Optional[list[str]],
    user: Optional[str],
) -> None:
    running_container = container.run_detached(
        tty=True,
        environment=env,
        command=cmd,
        user=user,
    )

    # sleeping some time to let the server start
    time_spent = 0.0
    wait_time = 0.1
    time_limit = 15
    while time_spent < time_limit:
        time.sleep(wait_time)
        time_spent += wait_time
        if get_health(running_container) == "healthy":
            raise RuntimeError("Container should not be healthy for these testcases.")

    assert get_health(running_container) != "healthy"
