# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging

import pytest
import os

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize("test_file, output_format,", [
    ("notebook_math", "pdf"), ("notebook_math", "html"),
    ("notebook_svg", "pdf"), ("notebook_svg", "html"),
])
def test_nbconvert(container, test_file, output_format):
    """Check if nbconvert is able to convert a notebook file"""
    host_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
    cont_data_dir = "/home/jovyan/data"
    output_dir = "/tmp"
    LOGGER.info(f"Test that the example notebook {test_file} can be converted to {output_format.upper()} ...")
    command = f"jupyter nbconvert {cont_data_dir}/{test_file}.ipynb --output-dir {output_dir} --to {output_format}"
    c = container.run(
        volumes={host_data_dir: {"bind": cont_data_dir, "mode": "ro"}},
        tty=True,
        command=["start.sh", "bash", "-c", command],
    )
    rv = c.wait(timeout=30)
    assert rv == 0 or rv["StatusCode"] == 0, f"Command {command} failed"
    logs = c.logs(stdout=True).decode("utf-8")
    LOGGER.debug(logs)
    expected_file = f"{output_dir}/{test_file}.{output_format}"
    assert expected_file in logs, f"Expected file {expected_file} not generated"
