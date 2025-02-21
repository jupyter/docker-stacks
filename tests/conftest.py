# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
from collections.abc import Generator

import docker
import pytest  # type: ignore
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from tests.utils.tracked_container import TrackedContainer


@pytest.fixture(scope="session")
def http_client() -> requests.Session:
    """Requests session with retries and backoff."""
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1)
    s.mount("http://", HTTPAdapter(max_retries=retries))
    s.mount("https://", HTTPAdapter(max_retries=retries))
    return s


@pytest.fixture(scope="session")
def docker_client() -> docker.DockerClient:
    """Docker client configured based on the host environment"""
    return docker.from_env()


@pytest.fixture(scope="session")
def image_name() -> str:
    """Image name to test"""
    return os.environ["TEST_IMAGE"]


@pytest.fixture(scope="function")
def container(
    docker_client: docker.DockerClient, image_name: str
) -> Generator[TrackedContainer]:
    """Notebook container with initial configuration appropriate for testing
    (e.g., HTTP port exposed to the host for HTTP calls).

    Yields the container instance and kills it when the caller is done with it.
    """
    container = TrackedContainer(
        docker_client,
        image_name,
        detach=True,
    )
    yield container
    container.remove()
