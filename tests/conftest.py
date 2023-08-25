# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
import os
import socket
from contextlib import closing
from typing import Any, Optional

import docker
import pytest  # type: ignore
import requests
from docker.models.containers import Container
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

LOGGER = logging.getLogger(__name__)


def find_free_port() -> str:
    """Returns the available host port. Can be called in multiple threads/processes."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]  # type: ignore


def get_health(container: Container) -> str:
    api_client = docker.APIClient()
    inspect_results = api_client.inspect_container(container.name)
    return inspect_results["State"]["Health"]["Status"]  # type: ignore


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


class TrackedContainer:
    """Wrapper that collects docker container configuration and delays
    container creation/execution.

    Parameters
    ----------
    docker_client: docker.DockerClient
        Docker client instance
    image_name: str
        Name of the docker image to launch
    **kwargs: dict, optional
        Default keyword arguments to pass to docker.DockerClient.containers.run
    """

    def __init__(
        self,
        docker_client: docker.DockerClient,
        image_name: str,
        **kwargs: Any,
    ):
        self.container: Optional[Container] = None
        self.docker_client: docker.DockerClient = docker_client
        self.image_name: str = image_name
        self.kwargs: Any = kwargs

    def run_detached(self, **kwargs: Any) -> Container:
        """Runs a docker container using the preconfigured image name
        and a mix of the preconfigured container options and those passed
        to this method.

        Keeps track of the docker.Container instance spawned to kill it
        later.

        Parameters
        ----------
        **kwargs: dict, optional
            Keyword arguments to pass to docker.DockerClient.containers.run
            extending and/or overriding key/value pairs passed to the constructor

        Returns
        -------
        docker.Container
        """
        all_kwargs = self.kwargs | kwargs
        LOGGER.info(f"Running {self.image_name} with args {all_kwargs} ...")
        self.container = self.docker_client.containers.run(
            self.image_name,
            **all_kwargs,
        )
        return self.container

    def run_and_wait(
        self,
        timeout: int,
        no_warnings: bool = True,
        no_errors: bool = True,
        no_failure: bool = True,
        **kwargs: Any,
    ) -> str:
        running_container = self.run_detached(**kwargs)
        rv = running_container.wait(timeout=timeout)
        logs = running_container.logs().decode("utf-8")
        assert isinstance(logs, str)
        LOGGER.debug(logs)
        if no_warnings:
            assert not self.get_warnings(logs)
        if no_errors:
            assert not self.get_errors(logs)
        assert no_failure == (rv["StatusCode"] == 0)
        return logs

    @staticmethod
    def get_errors(logs: str) -> list[str]:
        return TrackedContainer._lines_starting_with(logs, "ERROR")

    @staticmethod
    def get_warnings(logs: str) -> list[str]:
        return TrackedContainer._lines_starting_with(logs, "WARNING")

    @staticmethod
    def _lines_starting_with(logs: str, pattern: str) -> list[str]:
        return [line for line in logs.splitlines() if line.startswith(pattern)]

    def remove(self) -> None:
        """Kills and removes the tracked docker container."""
        if self.container:
            self.container.remove(force=True)


@pytest.fixture(scope="function")
def container(docker_client: docker.DockerClient, image_name: str) -> Container:
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
