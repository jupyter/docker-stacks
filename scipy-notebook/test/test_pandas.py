# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

import pytest

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "name,command_list",
    [
        (
            "Sum series",
            [
                "import pandas as pd",
                "import numpy as np",
                "np.random.seed(0)",
                "print(pd.Series(np.random.randint(0, 7, size=10)).sum())"
            ]
        ),
    ],
)
def test_pandas(container, name, command_list):
    """Basic pandas tests"""
    LOGGER.info(f"Testing pandas: {name} ...")
    command = ';'.join(command_list)
    c = container.run(tty=True, command=["start.sh", "python", "-c", command])
    rv = c.wait(timeout=30)
    assert rv == 0 or rv["StatusCode"] == 0, f"Command {command} failed"
    logs = c.logs(stdout=True).decode("utf-8")
    LOGGER.debug(logs)
