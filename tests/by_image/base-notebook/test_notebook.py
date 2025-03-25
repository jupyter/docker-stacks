# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import requests

from tests.utils.tracked_container import TrackedContainer


def test_secured_server(
    container: TrackedContainer, http_client: requests.Session, free_host_port: int
) -> None:
    """Jupyter Server should eventually request user login."""
    container.run_detached(ports={"8888/tcp": free_host_port})
    resp = http_client.get(f"http://localhost:{free_host_port}")
    resp.raise_for_status()
    assert "login_submit" in resp.text, "User login not requested"
