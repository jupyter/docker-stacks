# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

import pytest

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "name,command",
    [
        (
            "Hello world",
            "import tensorflow as tf;print(tf.constant('Hello, TensorFlow'))",
        ),
        (
            "Sum",
            "import tensorflow as tf;print(tf.reduce_sum(tf.random.normal([1000, 1000])))",
        ),
    ],
)
def test_tensorflow(container, name, command):
    """Basic tensorflow tests"""
    LOGGER.info(f"Testing tensorflow: {name} ...")
    c = container.run(tty=True, command=["start.sh", "python", "-c", command])
    rv = c.wait(timeout=30)
    assert rv == 0 or rv["StatusCode"] == 0, f"Command {command} failed"
    logs = c.logs(stdout=True).decode("utf-8")
    LOGGER.debug(logs)
