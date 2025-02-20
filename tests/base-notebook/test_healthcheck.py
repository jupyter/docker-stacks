# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
import time

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
        (["JUPYTER_RUNTIME_DIR=/tmp/jupyter-runtime"], ["start-notebook.sh"], None),
        (
            [
                "NB_USER=testuser",
                "CHOWN_HOME=1",
                "JUPYTER_RUNTIME_DIR=/tmp/jupyter-runtime",
            ],
            ["start-notebook.sh"],
            "root",
        ),
    ],
)
def test_healthy(
    container: TrackedContainer,
    env: list[str] | None,
    cmd: list[str] | None,
    user: str | None,
) -> None:
    running_container = container.run_detached(
        tty=True,
        environment=env,
        command=cmd,
        user=user,
    )

    # giving some time to let the server start
    finish_time = time.time() + 10
    sleep_time = 0.1
    while time.time() < finish_time:
        time.sleep(sleep_time)
        if get_health(running_container) == "healthy":
            return

    assert get_health(running_container) == "healthy"


@pytest.mark.parametrize(
    "env,cmd,user",
    [
        (
            [
                "HTTPS_PROXY=https://host.docker.internal",
                "HTTP_PROXY=http://host.docker.internal",
            ],
            None,
            None,
        ),
        (
            [
                "NB_USER=testuser",
                "CHOWN_HOME=1",
                "JUPYTER_PORT=8123",
                "HTTPS_PROXY=https://host.docker.internal",
                "HTTP_PROXY=http://host.docker.internal",
            ],
            ["start-notebook.py", "--ServerApp.base_url=/test"],
            "root",
        ),
    ],
)
def test_healthy_with_proxy(
    container: TrackedContainer,
    env: list[str] | None,
    cmd: list[str] | None,
    user: str | None,
) -> None:
    running_container = container.run_detached(
        tty=True,
        environment=env,
        command=cmd,
        user=user,
    )

    # giving some time to let the server start
    finish_time = time.time() + 10
    sleep_time = 0.1
    while time.time() < finish_time:
        time.sleep(sleep_time)
        if get_health(running_container) == "healthy":
            return

    assert get_health(running_container) == "healthy"


@pytest.mark.parametrize(
    "env,cmd",
    [
        (["NB_USER=testuser", "CHOWN_HOME=1"], None),
        (
            ["NB_USER=testuser", "CHOWN_HOME=1"],
            ["start-notebook.py", "--ServerApp.base_url=/test"],
        ),
        (
            ["NB_USER=testuser", "CHOWN_HOME=1", "JUPYTER_PORT=8123"],
            ["start-notebook.py", "--ServerApp.base_url=/test"],
        ),
    ],
)
def test_not_healthy(
    container: TrackedContainer,
    env: list[str] | None,
    cmd: list[str] | None,
) -> None:
    running_container = container.run_detached(
        tty=True,
        environment=env,
        command=cmd,
    )

    # giving some time to let the server start
    finish_time = time.time() + 5
    sleep_time = 0.1
    while time.time() < finish_time:
        time.sleep(sleep_time)
        if get_health(running_container) == "healthy":
            raise RuntimeError("Container should not be healthy for this testcase")

    assert get_health(running_container) != "healthy"
