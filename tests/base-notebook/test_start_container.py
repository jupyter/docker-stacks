# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
import time
from typing import Optional

import pytest  # type: ignore
import requests

from tests.conftest import TrackedContainer, find_free_port

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "env,expected_command,expected_start,expected_warnings",
    [
        (None, "jupyter lab", True, []),
        (["DOCKER_STACKS_JUPYTER_CMD=lab"], "jupyter lab", True, []),
        (["RESTARTABLE=yes"], "run-one-constantly jupyter lab", True, []),
        (["DOCKER_STACKS_JUPYTER_CMD=notebook"], "jupyter notebook", True, []),
        (["DOCKER_STACKS_JUPYTER_CMD=server"], "jupyter server", True, []),
        (["DOCKER_STACKS_JUPYTER_CMD=nbclassic"], "jupyter nbclassic", True, []),
        (
            ["JUPYTERHUB_API_TOKEN=my_token"],
            "jupyterhub-singleuser",
            False,
            ["WARNING: using start-singleuser.py"],
        ),
    ],
)
def test_start_notebook(
    container: TrackedContainer,
    http_client: requests.Session,
    env: Optional[list[str]],
    expected_command: str,
    expected_start: bool,
    expected_warnings: list[str],
) -> None:
    """Test the notebook start-notebook.py script"""
    LOGGER.info(
        f"Test that the start-notebook.py launches the {expected_command} server from the env {env} ..."
    )
    host_port = find_free_port()
    running_container = container.run_detached(
        tty=True,
        environment=env,
        ports={"8888/tcp": host_port},
    )
    # sleeping some time to let the server start
    time.sleep(1)
    logs = running_container.logs().decode("utf-8")
    LOGGER.debug(logs)
    # checking that the expected command is launched
    assert (
        f"Executing the command: {expected_command}" in logs
    ), f"Not the expected command ({expected_command}) was launched"
    # checking errors and warnings in logs
    assert "ERROR" not in logs, "ERROR(s) found in logs"
    for exp_warning in expected_warnings:
        assert exp_warning in logs, f"Expected warning {exp_warning} not found in logs"
    warnings = TrackedContainer.get_warnings(logs)
    assert len(expected_warnings) == len(warnings)
    # checking if the server is listening
    if expected_start:
        resp = http_client.get(f"http://localhost:{host_port}")
        assert resp.status_code == 200, "Server is not listening"


def test_tini_entrypoint(
    container: TrackedContainer, pid: int = 1, command: str = "tini"
) -> None:
    """Check that tini is launched as PID 1

    Credits to the following answer for the ps options used in the test:
    https://superuser.com/questions/632979/if-i-know-the-pid-number-of-a-process-how-can-i-get-its-name
    """
    LOGGER.info(f"Test that {command} is launched as PID {pid} ...")
    running_container = container.run_detached(
        tty=True,
        command=["start.sh"],
    )
    # Select the PID 1 and get the corresponding command
    cmd = running_container.exec_run(f"ps -p {pid} -o comm=")
    output = cmd.output.decode("utf-8").strip("\n")
    assert "ERROR" not in output
    assert "WARNING" not in output
    assert output == command, f"{command} shall be launched as pid {pid}, got {output}"
