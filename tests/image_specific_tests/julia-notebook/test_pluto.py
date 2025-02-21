# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import requests

from tests.shared_checks.pluto_check import check_pluto_proxy
from tests.utils.tracked_container import TrackedContainer


def test_pluto_proxy(
    container: TrackedContainer, http_client: requests.Session
) -> None:
    """Pluto proxy starts Pluto correctly"""
    check_pluto_proxy(container, http_client)
