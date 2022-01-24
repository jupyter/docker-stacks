# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

from packaging import version  # type: ignore

from conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)


def test_python_version(
    container: TrackedContainer, python_next_version: str = "3.10"
) -> None:
    """Check that python version is lower than the next version"""
    LOGGER.info(f"Checking that python version is lower than {python_next_version}")
    logs = container.run_and_wait(
        timeout=5,
        tty=True,
        command=["start.sh", "python", "--version"],
    )
    actual_python_version = version.parse(logs.split()[1])
    assert actual_python_version < version.parse(
        python_next_version
    ), f"Python version shall be lower than {python_next_version}"
