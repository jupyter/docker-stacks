# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.


import requests
from conftest import TrackedContainer


def test_secured_server(
    container: TrackedContainer, http_client: requests.Session
) -> None:
    """Notebook server should eventually request user login."""
    container.run()
    resp = http_client.get("http://localhost:8888")
    resp.raise_for_status()
    assert "login_submit" in resp.text, "User login not requested"
