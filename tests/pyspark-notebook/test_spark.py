# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

from tests.conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)


def test_spark_shell(container: TrackedContainer) -> None:
    """Checking if Spark (spark-shell) is running properly"""
    logs = container.run_and_wait(
        timeout=60,
        tty=True,
        command=["start.sh", "bash", "-c", 'spark-shell <<< "1+1"'],
    )

    assert "res0: Int = 2" in logs, "spark-shell does not work"


def test_pandas_version(container: TrackedContainer) -> None:
    """Checking if pandas is installed and its version is 1.5.3
    This is only needed for Spark before 4.0 see #1924"""
    command = [
        "start.sh",
        "bash",
        "-c",
        "python -c 'import pandas; print(pandas.__version__)'",
    ]
    logs = container.run_and_wait(
        timeout=60,
        tty=True,
        command=command,
    )

    assert "1.5.3" in logs, "pandas version is not 1.5.3"
