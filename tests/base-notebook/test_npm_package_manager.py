# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging

from tests.conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)


def test_npm_package_manager(container: TrackedContainer) -> None:
    """Test the notebook start-notebook script"""
    LOGGER.info("Test that the package manager npm is working properly ...")
    container.run_and_wait(
        timeout=5,
        tty=True,
        command=["start.sh", "bash", "-c", "npm --version"],
    )
