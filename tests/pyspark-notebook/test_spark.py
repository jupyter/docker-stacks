# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

from tests.conftest import TrackedContainer
from tests.run_command import run_command

LOGGER = logging.getLogger(__name__)


def test_spark_shell(container: TrackedContainer) -> None:
    """Checking if Spark (spark-shell) is running properly"""
    logs = run_command(container, 'spark-shell <<< "1+1"', timeout=60)
    assert "res0: Int = 2" in logs, "spark-shell does not work"
