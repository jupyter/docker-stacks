# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import logging
import typing

import docker
from docker.models.containers import Container
import pytest
import requests

from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


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
    return docker.from_env()


@pytest.fixture(scope="session")
def image_name() -> str:
    """Image name to test"""
    return os.getenv("TEST_IMAGE")


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
        self, docker_client: docker.DockerClient, image_name: str, **kwargs: typing.Any
    ):
        self.container = None
        self.docker_client = docker_client
        self.image_name = image_name
        self.kwargs = kwargs

    def run_detached(self, **kwargs: typing.Any) -> Container:
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
        **kwargs: typing.Any,
    ) -> str:
        running_container = self.run_and_wait(**kwargs)
        rv = running_container.wait(timeout=timeout)
        logs = running_container.logs().decode("utf-8")
        LOGGER.debug(logs)
        if no_warnings:
            assert "WARNING" not in logs
        if no_errors:
            assert "ERROR" not in logs
        assert rv == 0 or rv["StatusCode"] == 0
        return logs

    def remove(self):
        """Kills and removes the tracked docker container."""
        if self.container:
            self.container.remove(force=True)


@pytest.fixture(scope="function")
def container(docker_client: docker.DockerClient, image_name: str):
    """Notebook container with initial configuration appropriate for testing
    (e.g., HTTP port exposed to the host for HTTP calls).

    Yields the container instance and kills it when the caller is done with it.
    """
    container = TrackedContainer(
        docker_client,
        image_name,
        detach=True,
        ports={"8888/tcp": 8888},
    )
    yield container
    container.remove()
