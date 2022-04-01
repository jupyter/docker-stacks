# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

from conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)


def test_spark_shell(container: TrackedContainer) -> None:
    """Checking if Spark (spark-shell) is running properly"""
    logs = container.run_and_wait(
        timeout=60,
        no_warnings=False,
        tty=True,
        command=["start.sh", "bash", "-c", 'spark-shell <<< "1+1"'],
    )
    warnings = TrackedContainer.get_warnings(logs)
    # Some Spark warnings
    assert len(warnings) == 5

    assert "res0: Int = 2" in logs, "spark-shell does not work"
