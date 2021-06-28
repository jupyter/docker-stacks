# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging

LOGGER = logging.getLogger(__name__)


def test_inkscape(container):
    """Inkscape shall be installed to be able to convert SVG files."""
    LOGGER.info("Test that inkscape is working by printing its version ...")
    c = container.run(
        tty=True,
        command=["start.sh", "bash", "-c", "inkscape --version"],
    )
    c.wait(timeout=10)
    logs = c.logs(stdout=True).decode("utf-8")
    LOGGER.debug(logs)
    assert "Inkscape" in logs, "Inkscape not installed or not working"
