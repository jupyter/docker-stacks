# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging
import os

LOGGER = logging.getLogger(__name__)
THIS_DIR = os.path.dirname(os.path.realpath(__file__))


def test_units(container):
    """Various units tests
    Add a py file in the {image}/test/units dir and it will be automatically tested
    """
    short_image_name = container.image_name[container.image_name.find('/') + 1:]
    host_data_dir = os.path.join(THIS_DIR, f"../{short_image_name}/test/units")
    LOGGER.info(f"Searching for units tests in {host_data_dir}")
    cont_data_dir = "/home/jovyan/data"

    if not os.path.exists(host_data_dir):
        LOGGER.info(f"Not found unit tests for image: {container.image_name}")
        return

    command = "sleep infinity"
    running_container = container.run(
        volumes={host_data_dir: {"bind": cont_data_dir, "mode": "ro"}},
        tty=True,
        command=["start.sh", "bash", "-c", command],
    )
    for test_file in os.listdir(host_data_dir):
        LOGGER.info(f"Running unit test: {test_file}")
        command = f"python {cont_data_dir}/{test_file}"
        cmd = running_container.exec_run(command)
        assert cmd.exit_code == 0, f"Command {command} failed"
        LOGGER.debug(cmd.output.decode("utf-8"))
