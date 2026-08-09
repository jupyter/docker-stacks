# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from pathlib import Path

import pytest

from tests.shared_checks.nbconvert_check import check_nbconvert
from tests.utils.tracked_container import TrackedContainer

LOGGER = logging.getLogger(__name__)
THIS_DIR = Path(__file__).parent.resolve()


@pytest.mark.parametrize("test_file", ["notebook_math", "notebook_svg"])
@pytest.mark.parametrize("output_format", ["pdf", "html", "markdown"])
def test_nbconvert(
    container: TrackedContainer, test_file: str, output_format: str
) -> None:
    host_data_file = THIS_DIR / "data" / f"{test_file}.ipynb"
    check_nbconvert(container, host_data_file, output_format, execute=False)


def test_nbconvert_execute(container: TrackedContainer) -> None:
    """A trivial notebook should be executed through the python3 kernel"""
    host_data_file = THIS_DIR / "data" / "execute_python.ipynb"
    check_nbconvert(container, host_data_file, "markdown", execute=True)
