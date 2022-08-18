# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from tests.conftest import TrackedContainer
from tests.R_minetype_check import minetypes_check


def test_minetypes(container: TrackedContainer) -> None:
    """Check if Rscript command for minetypes can be executed"""
    logs = minetypes_check(container)
    assert len(logs) == 0, "Command R command failed"
