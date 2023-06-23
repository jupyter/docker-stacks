# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging
from pathlib import Path

import pytest  # type: ignore

from tests.conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)
THIS_DIR = Path(__file__).parent.resolve()


@pytest.mark.parametrize(
    "test_file",
    ["issue_1168", "local_pyspark", "local_sparklyr", "local_sparkR"],
)
def test_nbconvert(container: TrackedContainer, test_file: str) -> None:
    """Check if Spark notebooks can be executed"""
    host_data_dir = THIS_DIR / "data"
    cont_data_dir = "/home/jovyan/data"
    output_dir = "/tmp"
    conversion_timeout_ms = 600
    LOGGER.info(f"Test that {test_file} notebook can be executed ...")
    command = (
        "jupyter nbconvert --to markdown "
        + f"--ExecutePreprocessor.timeout={conversion_timeout_ms} "
        + f"--output-dir {output_dir} "
        + f"--execute {cont_data_dir}/{test_file}.ipynb"
    )
    logs = container.run_and_wait(
        timeout=60,
        volumes={str(host_data_dir): {"bind": cont_data_dir, "mode": "ro"}},
        tty=True,
        command=["start.sh", "bash", "-c", command],
    )

    expected_file = f"{output_dir}/{test_file}.md"
    assert expected_file in logs, f"Expected file {expected_file} not generated"


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
