# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

import pytest  # type: ignore
import requests

from tests.utils.tracked_container import TrackedContainer
from tests.utils.wait import wait_until

LOGGER = logging.getLogger(__name__)


def test_cli_args(
    container: TrackedContainer, http_client: requests.Session, free_host_port: int
) -> None:
    """Image should respect command line args (e.g., disabling token security)"""
    container.run_detached(
        command=["start-notebook.py", "--IdentityProvider.token=''"],
        ports={"8888/tcp": free_host_port},
    )
    resp = http_client.get(f"http://localhost:{free_host_port}", timeout=10)
    resp.raise_for_status()
    logs = container.get_logs()
    LOGGER.debug(logs)
    assert not TrackedContainer.get_errors(logs)
    assert not TrackedContainer.get_warnings(logs)
    assert "login_submit" not in resp.text


def test_nb_user_change(container: TrackedContainer) -> None:
    """Container should change the username (`NB_USER`) of the default user."""
    nb_user = "nayvoj"
    container.run_detached(
        user="root",
        environment=[f"NB_USER={nb_user}", "CHOWN_HOME=yes"],
        command=["sleep", "infinity"],
    )

    # Wait until the start script has finished preparing the user:
    # the rename, home copy, and chown all happen before this line is logged.
    # We can't wait for the container itself, because it sleeps forever.
    assert wait_until(
        lambda: f"Running as {nb_user}:" in container.get_logs(), timeout=30
    ), "start.sh didn't finish preparing the user"
    LOGGER.info(
        f"Checking if a home folder of {nb_user} contains the hidden '.jupyter' folder with appropriate permissions ..."
    )
    command = f'stat -c "%F %U %G" /home/{nb_user}/.jupyter'
    expected_output = f"directory {nb_user} users"
    output = container.exec_cmd(command, workdir=f"/home/{nb_user}")
    assert (
        output == expected_output
    ), f"Hidden folder .jupyter was not copied properly to {nb_user} home folder. stat: {output}, expected {expected_output}"


@pytest.mark.filterwarnings("ignore:Unverified HTTPS request")
def test_unsigned_ssl(
    container: TrackedContainer, http_client: requests.Session, free_host_port: int
) -> None:
    """Container should generate a self-signed SSL certificate
    and Jupyter Server should use it to enable HTTPS.
    """
    container.run_detached(
        environment=["GEN_CERT=yes"],
        ports={"8888/tcp": free_host_port},
    )
    url = f"https://localhost:{free_host_port}"

    def server_answers() -> bool:
        try:
            return http_client.get(url, verify=False, timeout=10).status_code == 200
        except requests.RequestException:
            return False

    # NOTE: The requests.Session backing the http_client fixture
    # does not retry properly while the server is booting up.
    # An SSL handshake error seems to abort the retry logic,
    # so tolerate SSL/connection errors here until the server answers.
    assert wait_until(server_answers, timeout=60), "Server did not start"
    resp = http_client.get(url, verify=False, timeout=10)
    resp.raise_for_status()
    assert "login_submit" in resp.text
    logs = container.get_logs()
    assert not TrackedContainer.get_errors(logs)
    assert not TrackedContainer.get_warnings(logs)


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
    free_host_port: int,
    env: dict[str, str],
) -> None:
    """Container should be accessible from the host
    when using custom internal port"""
    internal_port = env.get("JUPYTER_PORT", 8888)
    container.run_detached(
        command=["start-notebook.py", "--IdentityProvider.token=''"],
        environment=env,
        ports={internal_port: free_host_port},
    )
    resp = http_client.get(f"http://localhost:{free_host_port}", timeout=10)
    resp.raise_for_status()
    logs = container.get_logs()
    LOGGER.debug(logs)
    assert not TrackedContainer.get_errors(logs)
    assert not TrackedContainer.get_warnings(logs)
