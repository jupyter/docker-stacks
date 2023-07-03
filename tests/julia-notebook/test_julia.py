# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from tests.conftest import TrackedContainer
from tests.run_command import run_command


def test_julia(container: TrackedContainer) -> None:
    run_command(container, "julia --version")
