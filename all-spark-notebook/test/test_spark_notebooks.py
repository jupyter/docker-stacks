# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging

import pytest
import os

LOGGER = logging.getLogger(__name__)
THIS_DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.parametrize(
    "test_file",
    # TODO: add local_sparklyr
    ["local_pyspark", "local_spylon", "local_sparkR", "issue_1168"],
)
def test_nbconvert(container, test_file):
    """Check if Spark notebooks can be executed"""
    host_data_dir = os.path.join(THIS_DIR, "data")
    cont_data_dir = "/home/jovyan/data"
    output_dir = "/tmp"
    timeout_ms = 600
    LOGGER.info(f"Test that {test_file} notebook can be executed ...")
    command = (
        "jupyter nbconvert --to markdown "
        + f"--ExecutePreprocessor.timeout={timeout_ms} "
        + f"--output-dir {output_dir} "
        + f"--execute {cont_data_dir}/{test_file}.ipynb"
    )
    c = container.run(
        volumes={host_data_dir: {"bind": cont_data_dir, "mode": "ro"}},
        tty=True,
        command=["start.sh", "bash", "-c", command],
    )
    rv = c.wait(timeout=timeout_ms / 10 + 10)
    logs = c.logs(stdout=True).decode("utf-8")
    LOGGER.debug(logs)
    assert rv == 0 or rv["StatusCode"] == 0, f"Command {command} failed"
    expected_file = f"{output_dir}/{test_file}.md"
    assert expected_file in logs, f"Expected file {expected_file} not generated"
