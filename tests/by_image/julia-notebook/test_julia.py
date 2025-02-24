# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from tests.utils.run_command import run_command
from tests.utils.tracked_container import TrackedContainer


def test_julia(container: TrackedContainer) -> None:
    run_command(container, "julia --version")
