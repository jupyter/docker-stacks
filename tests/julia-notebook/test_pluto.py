import logging
import secrets
import time

import requests

from tests.conftest import TrackedContainer, find_free_port

LOGGER = logging.getLogger(__name__)


def test_pluto_proxy(
    container: TrackedContainer, http_client: requests.Session
) -> None:
    """Pluto proxy starts Pluto correctly"""
    host_port = find_free_port()
    token = secrets.token_hex()
    container.run_detached(
        command=[
            "start.sh",
            "jupyter",
            "lab",
            "--port=8888",
            f"--LabApp.token={token}",
        ],
        ports={"8888/tcp": host_port},
    )
    # Give the server a bit of time to start
    time.sleep(3)
    resp = http_client.get(f"http://localhost:{host_port}/pluto?token={token}")
    resp.raise_for_status()
    assert "Pluto.jl notebooks" in resp.text, "Pluto.jl text not found in /pluto page"
