# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from collections.abc import Generator
from pathlib import Path
from random import randint

import docker
import pytest  # type: ignore

from tests.utils.tracked_container import TrackedContainer

LOGGER = logging.getLogger(__name__)
THIS_DIR = Path(__file__).parent.resolve()


@pytest.fixture(scope="session")
def ipv6_network(docker_client: docker.DockerClient) -> Generator[str, None, None]:
    """Create a dual-stack IPv6 docker network"""
    # Doesn't have to be routable since we're testing inside the container
    subnet64 = "fc00:" + ":".join(hex(randint(0, 2**16))[2:] for _ in range(3))
    name = subnet64.replace(":", "-")
    docker_client.networks.create(
        name,
        ipam=docker.types.IPAMPool(
            subnet=subnet64 + "::/64",
            gateway=subnet64 + "::1",
        ),
        enable_ipv6=True,
        internal=True,
    )
    yield name
    docker_client.networks.get(name).remove()


def test_ipv46(container: TrackedContainer, ipv6_network: str) -> None:
    """Check server is listening on the expected IP families"""
    host_data_dir = THIS_DIR / "data"
    cont_data_dir = "/home/jovyan/data"
    LOGGER.info("Testing that server is listening on IPv4 and IPv6 ...")
    running_container = container.run_detached(
        network=ipv6_network,
        volumes={str(host_data_dir): {"bind": cont_data_dir, "mode": "ro,z"}},
        tty=True,
    )

    command = ["python", "./data/check_listening.py"]
    r = running_container.exec_run(command)
    LOGGER.info(r.output.decode())
    assert r.exit_code == 0
