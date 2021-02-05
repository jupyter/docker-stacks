# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

import pytest

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "name,command",
    [
        (
            "Hello SensiML",
            "import sensiml;print(sensiml.name)",
        ),
        (
            "Widget Modules Length",
            "import sensiml;print(len(dir(sensiml.widgets)) > 0)",
        ),
    ],
)
def test_sensiml(container, name, command):
    """Basic SensiML tests"""
    LOGGER.info(f"Testing SensiML: {name} ...")
    c = container.run(tty=True, command=["start.sh", "python", "-c", command])
    rv = c.wait(timeout=30)
    assert rv == 0 or rv["StatusCode"] == 0, f"Command {command} failed"
    logs = c.logs(stdout=True).decode("utf-8")
    LOGGER.debug(logs)
