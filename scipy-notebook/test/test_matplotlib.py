# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging

import pytest
import os

LOGGER = logging.getLogger(__name__)


def test_matplotlib(container):
    """Test that matplotlib is able to plot a graph and write it as an image"""
    host_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
    cont_data_dir = "/home/jovyan/data"
    test_file = "matplotlib_1.py"
    output_dir = "/tmp"
    LOGGER.info(f"Test that matplotlib is able to plot a graph and write it as an image ...")
    command = "sleep infinity"
    running_container = container.run(
        volumes={host_data_dir: {"bind": cont_data_dir, "mode": "ro"}},
        tty=True,
        command=["start.sh", "bash", "-c", command],
    )
    command = f"python {cont_data_dir}/{test_file}"
    cmd = running_container.exec_run(command)
    assert cmd.exit_code == 0, f"Command {command} failed"
    LOGGER.debug(cmd.output.decode("utf-8"))
    # Checking if the file is generated
    # https://stackoverflow.com/a/15895594/4413446
    expected_file = f"{output_dir}/test.png"
    command = f"test -s {expected_file}"
    cmd = running_container.exec_run(command)
    assert cmd.exit_code == 0, f"Command {command} failed"
    LOGGER.debug(cmd.output.decode("utf-8"))
