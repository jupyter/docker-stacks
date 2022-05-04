# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

from tests.conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)


def test_julia(container: TrackedContainer) -> None:
    """Basic julia test"""
    LOGGER.info("Test that julia is correctly installed ...")
    logs = container.run_and_wait(
        timeout=5,
        tty=True,
        command=["start.sh", "bash", "-c", "julia --version"],
    )
    LOGGER.debug(logs)
