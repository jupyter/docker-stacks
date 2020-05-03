# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging

import pytest
import os

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize("format", ["html", "pdf"])
def test_nbconvert(container, format):
    """Check if nbconvert is able to convert a notebook file"""
    host_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
    cont_data_dir = "/home/jovyan/data"
    test_file = "notebook1"
    output_dir = "/tmp"
    LOGGER.info(f"Test that an example notebook can be converted to {format.upper()} ...")
    command = f"jupyter nbconvert {cont_data_dir}/{test_file}.ipynb --output-dir {output_dir} --to {format}"
    c = container.run(
        volumes={host_data_dir: {"bind": cont_data_dir, "mode": "ro"}},
        tty=True,
        command=["start.sh", "bash", "-c", command],
    )
    rv = c.wait(timeout=30)
    assert rv == 0 or rv["StatusCode"] == 0, f"Command {command} failed"
    logs = c.logs(stdout=True).decode("utf-8")
    LOGGER.debug(logs)
    expected_file = f"{output_dir}/{test_file}.{format}"
    assert expected_file in logs, f"Expected file {expected_file} not generated"
