# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging

from conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)


def test_inkscape(container: TrackedContainer) -> None:
    """Inkscape shall be installed to be able to convert SVG files."""
    LOGGER.info("Test that inkscape is working by printing its version ...")
    logs = container.run_and_wait(
        timeout=10,
        tty=True,
        command=["start.sh", "bash", "-c", "inkscape --version"],
    )
    assert "Inkscape" in logs, "Inkscape not installed or not working"
