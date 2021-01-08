# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging
import pytest

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "env,expected_server",
    [
        (["JUPYTER_ENABLE_NB=yes"], "notebook"),
        (["JUPYTER_ENABLE_LAB=yes"], "lab"),
        (None, "lab"),
    ],
)
def test_start_notebook(container, http_client, env, expected_server):
    """Test the notebook start-notebook script"""
    LOGGER.info(
        f"Test that the start-notebook launches the {expected_server} server from the env {env} ..."
    )
    c = container.run(tty=True, environment=env, command=["start-notebook.sh"])
    resp = http_client.get("http://localhost:8888")
    assert resp.status_code == 200, "Server is not listening"
    logs = c.logs(stdout=True).decode("utf-8")
    LOGGER.debug(logs)
    assert (
        f"Executing the command: jupyter {expected_server}" in logs
    ), f"Not the expected command (jupyter {expected_server}) was launched"
    if env:
        # Checking warning messages
        if "JUPYTER_ENABLE_LAB=yes" in env:
            msg = "WARN: The JUPYTER_ENABLE_LAB environment variable is not required anymore"
        elif "JUPYTER_ENABLE_NB=yes" in env:
            msg = "WARN: We encourage users to transition to JupyterLab, Notebook support could be removed"
        assert msg in logs, f"Expected warning message {msg} not printed"
