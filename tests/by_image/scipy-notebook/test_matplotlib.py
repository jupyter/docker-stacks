# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from pathlib import Path

import pytest  # type: ignore

from tests.utils.tracked_container import TrackedContainer

LOGGER = logging.getLogger(__name__)
THIS_DIR = Path(__file__).parent.resolve()


@pytest.mark.parametrize(
    "test_file,expected_file,description",
    [
        (
            "matplotlib_1.py",
            "test.png",
            "Test that matplotlib can plot a graph and write it as an image ...",
        ),
        (
            "matplotlib_fonts_1.py",
            "test_fonts.png",
            "Test cm-super latex labels in matplotlib ...",
        ),
    ],
)
def test_matplotlib(
    container: TrackedContainer, test_file: str, expected_file: str, description: str
) -> None:
    """Various tests performed on matplotlib

    - Test that matplotlib is able to plot a graph and write it as an image
    - Test matplotlib latex fonts, which depend on the cm-super package
    """
    host_data_dir = THIS_DIR / "data/matplotlib"
    cont_data_dir = "/home/jovyan/data"
    output_dir = "/tmp"
    LOGGER.info(description)
    container.run_detached(
        volumes={str(host_data_dir): {"bind": cont_data_dir, "mode": "ro"}},
        command=["sleep", "infinity"],
    )

    command = f"python {cont_data_dir}/{test_file}"
    container.exec_cmd(command)

    # Checking if the file is generated
    # https://stackoverflow.com/a/15895594/4413446
    command = f"test -s {output_dir}/{expected_file}"
    container.exec_cmd(command)
