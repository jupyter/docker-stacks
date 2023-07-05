# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import requests

from tests.conftest import TrackedContainer
from tests.pluto_check import check_pluto_proxy


def test_pluto_proxy(
    container: TrackedContainer, http_client: requests.Session
) -> None:
    """Pluto proxy starts Pluto correctly"""
    check_pluto_proxy(container, http_client)
