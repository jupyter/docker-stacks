# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
import time

import pytest  # type: ignore
import requests

from tests.conftest import TrackedContainer, find_free_port

LOGGER = logging.getLogger(__name__)


def test_cli_args(container: TrackedContainer, http_client: requests.Session) -> None:
    """Container should respect notebook server command line args
    (e.g., disabling token security)"""
    host_port = find_free_port()
    running_container = container.run_detached(
        command=["start-notebook.sh", "--NotebookApp.token=''"],
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


@pytest.mark.filterwarnings("ignore:Unverified HTTPS request")
def test_unsigned_ssl(
    container: TrackedContainer, http_client: requests.Session
) -> None:
    """Container should generate a self-signed SSL certificate
    and notebook server should use it to enable HTTPS.
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
