# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
import secrets

import requests

from tests.utils.tracked_container import TrackedContainer
from tests.utils.wait import wait_until

LOGGER = logging.getLogger(__name__)


def check_pluto_proxy(
    container: TrackedContainer, http_client: requests.Session, free_host_port: int
) -> None:
    token = secrets.token_hex()
    container.run_detached(
        command=[
            "start-notebook.py",
            f"--IdentityProvider.token={token}",
        ],
        ports={"8888/tcp": free_host_port},
    )
    url = f"http://localhost:{free_host_port}/pluto?token={token}"

    def pluto_answers() -> bool:
        try:
            return http_client.get(url, timeout=10).status_code == 200
        except requests.RequestException:
            return False

    # The Jupyter Server has to boot and the proxy has to spawn Pluto
    # (a julia process) on the first request, so give it generous time
    assert wait_until(pluto_answers, timeout=90), "Pluto proxy did not start"

    resp = http_client.get(url, timeout=10)
    resp.raise_for_status()
    assert "Pluto.jl notebooks" in resp.text, "Pluto.jl text not found in /pluto page"
