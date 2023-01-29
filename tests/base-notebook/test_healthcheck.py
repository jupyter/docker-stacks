# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging
import time
from typing import Optional

import pytest  # type: ignore

from tests.conftest import TrackedContainer, get_health

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "env,cmd,workdir",
    [
        (None, None, None),
        (["DOCKER_STACKS_JUPYTER_CMD=lab"], None, None),
        (["DOCKER_STACKS_JUPYTER_CMD=notebook"], None, None),
        (["DOCKER_STACKS_JUPYTER_CMD=server"], None, None),
        (["DOCKER_STACKS_JUPYTER_CMD=nbclassic"], None, None),
        (["RESTARTABLE=yes"], None, None),
        (["JUPYTER_PORT=8171"], None, None),
        (["JUPYTER_PORT=8117", "DOCKER_STACKS_JUPYTER_CMD=notebook"], None, None),
        (None, ["start-notebook.sh", "--NotebookApp.base_url=/test"], None),
        (None, ["start-notebook.sh", "--NotebookApp.base_url=/test/"], None),
        (["GEN_CERT=1"], ["start-notebook.sh", "--NotebookApp.base_url=/test"], None),
        (
            ["GEN_CERT=1", "JUPYTER_PORT=7891"],
            ["start-notebook.sh", "--NotebookApp.base_url=/test"],
            None,
        ),
        (["NB_USER=testuser", "CHOWN_HOME=1"], None, "/home/testuser"),
        (
            ["NB_USER=testuser", "CHOWN_HOME=1"],
            ["start-notebook.sh", "--NotebookApp.base_url=/test"],
            "/home/testuser",
        ),
        (
            ["NB_USER=testuser", "CHOWN_HOME=1", "JUPYTER_PORT=8123"],
            ["start-notebook.sh", "--NotebookApp.base_url=/test"],
            "/home/testuser",
        ),
    ],
)
def test_health(
    container: TrackedContainer,
    env: Optional[list[str]],
    cmd: Optional[list[str]],
    workdir: Optional[str],
) -> None:
    running_container = container.run_detached(
        tty=True,
        environment=env,
        command=cmd,
        working_dir=workdir,
    )
    # sleeping some time to let the server start
    time.sleep(15)
    assert get_health(running_container) == "healthy"
