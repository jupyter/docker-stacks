# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from tests.conftest import TrackedContainer
from tests.run_command import run_command


def test_npm_package_manager(container: TrackedContainer) -> None:
    """Test that npm is installed and runs."""
    run_command(container, "npm --version")
