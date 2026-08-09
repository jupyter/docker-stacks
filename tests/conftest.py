# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
import socket
from collections.abc import Generator
from contextlib import closing

import docker
import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from tests.utils.tracked_container import TrackedContainer

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def http_client() -> requests.Session:
    """Requests session with retries and backoff."""
    s = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        # Retry on gateway errors as well: jupyter-server-proxy answers
        # 502/503 while the proxied server is still spawning
        status_forcelist=[502, 503, 504],
        allowed_methods=["GET", "HEAD"],
    )
    s.mount("http://", HTTPAdapter(max_retries=retries))
    s.mount("https://", HTTPAdapter(max_retries=retries))
    return s


@pytest.fixture(scope="session")
def docker_client() -> docker.DockerClient:
    """Docker client configured based on the host environment"""
    client = docker.from_env()
    LOGGER.debug(f"Docker client created: {client.version()}")
    return client


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom command-line options to pytest."""
    parser.addoption(
        "--registry",
        required=True,
        choices=["docker.io", "quay.io"],
        help="Image registry",
    )
    parser.addoption(
        "--owner",
        required=True,
        help="Owner of the image",
    )
    parser.addoption(
        "--image",
        required=True,
        help="Short image name",
    )


@pytest.fixture(scope="session")
def image_name(request: pytest.FixtureRequest) -> str:
    """Image name to test"""

    def option(name: str) -> str:
        value = request.config.getoption(name)
        assert isinstance(value, str)
        return value

    return f"{option('--registry')}/{option('--owner')}/{option('--image')}"


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
    """Reserves a free port on the host machine for the duration of the test.

    We keep the socket bound (but not listening) while the test runs:
    the kernel then never hands the same port out to other test workers
    asking for an ephemeral port, while docker-proxy, which sets
    SO_REUSEADDR just like we do here, can still bind the same port to
    publish the container's port.
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        # Must be set before bind() for the reservation mechanism to work
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", 0))
        yield s.getsockname()[1]
