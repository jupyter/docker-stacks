# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

from conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)


def test_julia(container: TrackedContainer) -> None:
    """Basic julia test"""
    LOGGER.info("Test that julia is correctly installed ...")
    running_container = container.run_detached(
        tty=True,
        command=["start.sh", "bash", "-c", "sleep infinity"],
    )
    command = "julia --version"
    cmd = running_container.exec_run(command)
    output = cmd.output.decode("utf-8")
    LOGGER.debug(output)
    assert cmd.exit_code == 0, f"Command {command} failed {output}"
