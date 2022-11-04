# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging

from tests.conftest import TrackedContainer
from tests.package_helper import run_package_manager

LOGGER = logging.getLogger(__name__)


def test_npm_package_manager(container: TrackedContainer) -> None:
    """Test that npm is installed and runs."""
    run_package_manager(container, "npm", "--version")
