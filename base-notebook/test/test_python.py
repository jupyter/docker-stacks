# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

from packaging import version

from conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)


def test_python_version(
    container: TrackedContainer, python_next_version: str = "3.10"
) -> None:
    """Check that python version is lower than the next version"""
    LOGGER.info(f"Checking that python version is lower than {python_next_version}")
    c = container.run(
        tty=True,
        command=["start.sh"],
    )
    cmd = c.exec_run("python --version")
    output = cmd.output.decode("utf-8")
    assert "ERROR" not in output
    assert "WARNING" not in output
    actual_python_version = version.parse(output.split()[1])
    assert actual_python_version < version.parse(
        python_next_version
    ), f"Python version shall be lower than {python_next_version}"
