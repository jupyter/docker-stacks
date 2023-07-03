# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from pathlib import Path

import pytest  # type: ignore

from tests.conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)
THIS_DIR = Path(__file__).parent.resolve()


@pytest.mark.parametrize(
    "test_file, output_format",
    [
        ("notebook_math", "pdf"),
        ("notebook_math", "html"),
        ("notebook_svg", "pdf"),
        ("notebook_svg", "html"),
    ],
)
def test_nbconvert(
    container: TrackedContainer, test_file: str, output_format: str
) -> None:
    """Check if nbconvert is able to convert a notebook file"""
    host_data_dir = THIS_DIR / "data"
    cont_data_dir = "/home/jovyan/data"
    output_dir = "/tmp"
    LOGGER.info(
        f"Test that the example notebook {test_file} can be converted to {output_format} ..."
    )
    command = f"jupyter nbconvert {cont_data_dir}/{test_file}.ipynb --output-dir {output_dir} --to {output_format}"
    logs = container.run_and_wait(
        timeout=30,
        volumes={str(host_data_dir): {"bind": cont_data_dir, "mode": "ro"}},
        tty=True,
        command=["start.sh", "bash", "-c", command],
    )
    expected_file = f"{output_dir}/{test_file}.{output_format}"
    assert expected_file in logs, f"Expected file {expected_file} not generated"
