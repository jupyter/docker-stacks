# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging
import pytest

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "package_manager, cmd",
    [
        ("apt", "--version"),
        ("conda", "--version"),
        ("mamba", "--version"),
        ("npm", "--version"),
        ("pip", "--version"),
    ],
)
def test_package_manager(container, package_manager, cmd):
    """Test the notebook start-notebook script"""
    LOGGER.info(
        f"Test that the package manager {package_manager} is working properly ..."
    )
    c = container.run(
        tty=True, command=["start.sh", "bash", "-c", f"{package_manager} {cmd}"]
    )
    rv = c.wait(timeout=5)
    logs = c.logs(stdout=True).decode("utf-8")
    assert (
        rv == 0 or rv["StatusCode"] == 0
    ), f"Package manager {package_manager} not working"
    LOGGER.debug(logs)
