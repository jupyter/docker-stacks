# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from tests.conftest import TrackedContainer
from tests.R_mimetype_check import check_r_mimetypes


def test_mimetypes(container: TrackedContainer) -> None:
    """Check if Rscript command for mimetypes can be executed"""
    check_r_mimetypes(container)
