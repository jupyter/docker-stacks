# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import time

import docker
import pytest
import requests


@pytest.fixture(scope='session')
def docker_client():
    """Docker client to use"""
    return docker.from_env()


@pytest.fixture(scope='session')
def image_name():
    """Image name to test"""
    return os.getenv('TEST_IMAGE', 'jupyter/base-notebook')


@pytest.fixture(scope='function')
def nb_container(docker_client, image_name):
    """Notebook container to test"""
    container = docker_client.containers.run(
        image_name,
        detach=True,
        auto_remove=True,
        ports={
            '8888/tcp': 8888
        }
    )
    yield container
    container.kill()


def test_server_liveliness(nb_container):
    """Notebook server should eventually respond with HTTP 200 OK."""
    for i in range(10):
        try:
            resp = requests.get('http://localhost:8888')
        except requests.exceptions.ConnectionError:
            # Wait a bit and try again. Just because the docker container
            # is running doesn't mean the notebook server is ready to accept
            # connections inside it.
            time.sleep(i)
        else:
            assert resp.status_code == 200
            break
    else:
        assert False, 'could not connect to server'
