# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import logging

import docker
import pytest
import requests

from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def http_client():
    """Requests session with retries and backoff."""
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1)
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.mount('https://', HTTPAdapter(max_retries=retries))
    return s


@pytest.fixture(scope='session')
def docker_client():
    """Docker client configured based on the host environment"""
    return docker.from_env()


@pytest.fixture(scope='session')
def image_name():
    """Image name to test"""
    return os.getenv('TEST_IMAGE', 'jupyter/base-notebook')


class TrackedContainer(object):
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

    def __init__(self, docker_client, image_name, **kwargs):
        self.container = None
        self.docker_client = docker_client
        self.image_name = image_name
        self.kwargs = kwargs

    def run(self, **kwargs):
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
        all_kwargs = {}
        all_kwargs.update(self.kwargs)
        all_kwargs.update(kwargs)
        LOGGER.info(f"Running {self.image_name} with args {all_kwargs} ...")
        self.container = self.docker_client.containers.run(self.image_name, **all_kwargs)
        return self.container

    def remove(self):
        """Kills and removes the tracked docker container."""
        if self.container:
            self.container.remove(force=True)


@pytest.fixture(scope='function')
def container(docker_client, image_name):
    """Notebook container with initial configuration appropriate for testing
    (e.g., HTTP port exposed to the host for HTTP calls).

    Yields the container instance and kills it when the caller is done with it.
    """
    container = TrackedContainer(
        docker_client,
        image_name,
        detach=True,
        ports={
            '8888/tcp': 8888
        }
    )
    yield container
    container.remove()


@pytest.fixture
def arch(container):
    """Return the architecture of the image based on its tag"""
    # default
    arch = "amd64"
    # give something like this ['jupyter/base-notebook', 'arm64']
    split = container.image_name.split(":", 1)
    if len(split) > 1 and split[1] != "latest":
        # setting the architecture to the tag if not latest
        arch = split[1]
    return arch


@pytest.fixture(autouse=True)
def skip_by_arch(request, arch):
    """Define a skip_arch marker to skip tests that will not work on
    Inspired by https://stackoverflow.com/a/28198398/4413446
    """
    if request.node.get_closest_marker('skip_arch'):
        if arch in request.node.get_closest_marker('skip_arch').args[0]:
            pytest.skip(f"skipped on the {arch} architecture")
