# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from pathlib import Path

from tests.shared_checks.nbconvert_check import check_nbconvert
from tests.utils.tracked_container import TrackedContainer

LOGGER = logging.getLogger(__name__)
THIS_DIR = Path(__file__).parent.resolve()


def test_r_nbconvert(container: TrackedContainer) -> None:
    """A trivial notebook should be executed through the R (IRkernel) kernel"""
    host_data_file = THIS_DIR / "data" / "execute_r.ipynb"
    check_nbconvert(container, host_data_file, "markdown", execute=True)
