# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging

import pytest  # type: ignore
from conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "package_manager, version_arg",
    [
        ("apt", "--version"),
        ("conda", "--version"),
        ("mamba", "--version"),
        ("npm", "--version"),
        ("pip", "--version"),
    ],
)
def test_package_manager(
    container: TrackedContainer, package_manager: str, version_arg: tuple[str, ...]
) -> None:
    """Test the notebook start-notebook script"""
    LOGGER.info(
        f"Test that the package manager {package_manager} is working properly ..."
    )
    container.run_and_wait(
        timeout=5,
        tty=True,
        command=["start.sh", "bash", "-c", f"{package_manager} {version_arg}"],
    )
