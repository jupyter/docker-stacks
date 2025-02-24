# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import requests

from tests.utils.find_free_port import find_free_port
from tests.utils.tracked_container import TrackedContainer


def test_secured_server(
    container: TrackedContainer, http_client: requests.Session
) -> None:
    """Jupyter Server should eventually request user login."""
    host_port = find_free_port()
    container.run_detached(ports={"8888/tcp": host_port})
    resp = http_client.get(f"http://localhost:{host_port}")
    resp.raise_for_status()
    assert "login_submit" in resp.text, "User login not requested"
