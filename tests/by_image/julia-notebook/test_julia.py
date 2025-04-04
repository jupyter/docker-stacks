# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from tests.utils.tracked_container import TrackedContainer


def test_julia(container: TrackedContainer) -> None:
    container.run_and_wait(timeout=10, command=["julia", "--version"])
