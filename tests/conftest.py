# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
import os
import socket
from collections.abc import Generator
from contextlib import closing

import docker
import pytest  # type: ignore
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from tests.utils.tracked_container import TrackedContainer

LOGGER = logging.getLogger(__name__)


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
    client = docker.from_env()
    LOGGER.debug(f"Docker client created: {client.version()}")
    return client


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
    )
    yield container
    container.remove()


@pytest.fixture(scope="function")
def free_host_port() -> Generator[int]:
    """Finds a free port on the host machine"""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        yield s.getsockname()[1]
