# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
import time
from pathlib import Path

from docker.models.containers import Container

from tests.conftest import TrackedContainer, get_health

LOGGER = logging.getLogger(__name__)
THIS_DIR = Path(__file__).parent.resolve()


def wait_healthy(container: Container, timeout: int) -> None:
    finish_time = time.time() + timeout
    sleep_time = 1
    while time.time() < finish_time:
        time.sleep(sleep_time)
        if get_health(container) == "healthy":
            return

    raise Exception(f"Container {container.name} not healthy after {int} s")


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
