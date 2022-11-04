# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging

import pytest  # type: ignore

from tests.conftest import TrackedContainer
from tests.package_helper import run_package_manager

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "package_manager, version_arg",
    [
        ("apt", "--version"),
        ("conda", "--version"),
        ("mamba", "--version"),
        ("pip", "--version"),
    ],
)
def test_package_manager(
    container: TrackedContainer, package_manager: str, version_arg: str
) -> None:
    """Test that package managers are installed and run."""
    run_package_manager(container, package_manager, version_arg)
