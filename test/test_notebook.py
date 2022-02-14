# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.


import requests
from conftest import TrackedContainer


def test_secured_server(
    container: TrackedContainer, http_client: requests.Session
) -> None:
    """Notebook server should eventually request user login."""
    container.run_detached(ports={"8888/tcp": None})
    host_port = container.get_host_port("8888/tcp")
    resp = http_client.get("http://localhost:" + host_port)
    resp.raise_for_status()
    assert "login_submit" in resp.text, "User login not requested"
