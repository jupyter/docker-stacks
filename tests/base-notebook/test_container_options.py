# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
import time

import pytest  # type: ignore
import requests

from tests.conftest import TrackedContainer, find_free_port

LOGGER = logging.getLogger(__name__)


def test_cli_args(container: TrackedContainer, http_client: requests.Session) -> None:
    """Image should respect command line args (e.g., disabling token security)"""
    host_port = find_free_port()
    running_container = container.run_detached(
        command=["start-notebook.py", "--IdentityProvider.token=''"],
        ports={"8888/tcp": host_port},
    )
    resp = http_client.get(f"http://localhost:{host_port}")
    resp.raise_for_status()
    logs = running_container.logs().decode("utf-8")
    LOGGER.debug(logs)
    assert "ERROR" not in logs
    warnings = TrackedContainer.get_warnings(logs)
    assert not warnings
    assert "login_submit" not in resp.text


def test_nb_user_change(container: TrackedContainer) -> None:
    """Container should change the username (`NB_USER`) of the default user."""
    nb_user = "nayvoj"
    running_container = container.run_detached(
        tty=True,
        user="root",
        environment=[f"NB_USER={nb_user}", "CHOWN_HOME=yes"],
        command=["start.sh", "bash", "-c", "sleep infinity"],
    )

    # Give the chown time to complete.
    # Use sleep, not wait, because the container sleeps forever.
    time.sleep(1)
    LOGGER.info(
        f"Checking if home folder of {nb_user} contains the hidden '.jupyter' folder with appropriate permissions ..."
    )
    command = f'stat -c "%F %U %G" /home/{nb_user}/.jupyter'
    expected_output = f"directory {nb_user} users"
    cmd = running_container.exec_run(command, workdir=f"/home/{nb_user}")
    output = cmd.output.decode("utf-8").strip("\n")
    assert (
        output == expected_output
    ), f"Hidden folder .jupyter was not copied properly to {nb_user} home folder. stat: {output}, expected {expected_output}"


@pytest.mark.filterwarnings("ignore:Unverified HTTPS request")
def test_unsigned_ssl(
    container: TrackedContainer, http_client: requests.Session
) -> None:
    """Container should generate a self-signed SSL certificate
    and Jupyter Server should use it to enable HTTPS.
    """
    host_port = find_free_port()
    running_container = container.run_detached(
        environment=["GEN_CERT=yes"],
        ports={"8888/tcp": host_port},
    )
    # NOTE: The requests.Session backing the http_client fixture does not retry
    # properly while the server is booting up. An SSL handshake error seems to
    # abort the retry logic. Forcing a long sleep for the moment until I have
    # time to dig more.
    time.sleep(1)
    resp = http_client.get(f"https://localhost:{host_port}", verify=False)
    resp.raise_for_status()
    assert "login_submit" in resp.text
    logs = running_container.logs().decode("utf-8")
    assert "ERROR" not in logs
    warnings = TrackedContainer.get_warnings(logs)
    assert not warnings


@pytest.mark.parametrize(
    "env",
    [
        {},
        {"JUPYTER_PORT": 1234, "DOCKER_STACKS_JUPYTER_CMD": "lab"},
        {"JUPYTER_PORT": 2345, "DOCKER_STACKS_JUPYTER_CMD": "notebook"},
        {"JUPYTER_PORT": 3456, "DOCKER_STACKS_JUPYTER_CMD": "server"},
        {"JUPYTER_PORT": 4567, "DOCKER_STACKS_JUPYTER_CMD": "nbclassic"},
        {"JUPYTER_PORT": 5678, "RESTARTABLE": "yes"},
        {"JUPYTER_PORT": 6789},
        {"JUPYTER_PORT": 7890, "DOCKER_STACKS_JUPYTER_CMD": "notebook"},
    ],
)
def test_custom_internal_port(
    container: TrackedContainer,
    http_client: requests.Session,
    env: dict[str, str],
) -> None:
    """Container should be accessible from the host
    when using custom internal port"""
    host_port = find_free_port()
    internal_port = env.get("JUPYTER_PORT", 8888)
    running_container = container.run_detached(
        command=["start-notebook.py", "--IdentityProvider.token=''"],
        environment=env,
        ports={internal_port: host_port},
    )
    resp = http_client.get(f"http://localhost:{host_port}")
    resp.raise_for_status()
    logs = running_container.logs().decode("utf-8")
    LOGGER.debug(logs)
    assert "ERROR" not in logs
    warnings = TrackedContainer.get_warnings(logs)
    assert not warnings
