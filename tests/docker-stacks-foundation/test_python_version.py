# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

from tests.conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)
EXPECTED_PYTHON_VERSION = "3.11"


def test_python_version(container: TrackedContainer) -> None:
    LOGGER.info(
        f"Checking that python major.minor version is {EXPECTED_PYTHON_VERSION}"
    )
    logs = container.run_and_wait(
        timeout=5,
        tty=True,
        command=["python", "--version"],
    )
    assert logs.startswith("Python ")
    full_version = logs.split()[1]
    major_minor_version = full_version[: full_version.rfind(".")]

    assert major_minor_version == EXPECTED_PYTHON_VERSION
