# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

import pytest

from tests.utils.tracked_container import TrackedContainer
from tests.utils.wait import wait_until

LOGGER = logging.getLogger(__name__)


def verify_health_status(
    container: TrackedContainer,
    *,
    expected_status: str,
    env: list[str] | None,
    cmd: list[str] | None,
    user: str | None = None,
) -> None:
    container.run_detached(
        environment=env,
        command=cmd,
        user=user,
    )

    # Give the container generous time to reach the expected status,
    # the server can be slow to start under parallel test load
    assert wait_until(
        lambda: container.get_health() == expected_status, timeout=60
    ), f"Expected health status: {expected_status}, current status: {container.get_health()}"


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
    verify_health_status(
        container, expected_status="healthy", env=env, cmd=cmd, user=user
    )


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
    verify_health_status(
        container, expected_status="healthy", env=env, cmd=cmd, user=user
    )


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
    verify_health_status(container, expected_status="unhealthy", env=env, cmd=cmd)
