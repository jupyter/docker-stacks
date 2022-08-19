# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from tests.conftest import TrackedContainer
from tests.R_mimetype_check import mimetypes_check


def test_mimetypes(container: TrackedContainer) -> None:
    """Check if Rscript command for mimetypes can be executed"""
    logs = mimetypes_check(container)
    assert len(logs) == 0, "Command R command failed"
