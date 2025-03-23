# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

from tests.utils.tracked_container import TrackedContainer

LOGGER = logging.getLogger(__name__)


def run_command(
    container: TrackedContainer,
    command: str,
    timeout: int = 5,
) -> str:
    LOGGER.info(f"Test that the command '{command}' is working properly ...")
    return container.run_and_wait(
        timeout=timeout,
        command=["bash", "-c", command],
    )
