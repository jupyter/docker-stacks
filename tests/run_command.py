# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

from tests.conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)


def run_command(
    container: TrackedContainer,
    command: str,
) -> None:
    """Runs the given package manager with its version argument."""

    LOGGER.info(f"Test that the command '{command}' is working properly ...")
    container.run_and_wait(
        timeout=5,
        tty=True,
        command=["start.sh", "bash", "-c", command],
    )
