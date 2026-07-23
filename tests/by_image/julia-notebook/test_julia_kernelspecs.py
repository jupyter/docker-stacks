# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from tests.shared_checks.kernelspec_check import check_kernelspecs
from tests.utils.tracked_container import TrackedContainer


def test_kernelspecs(container: TrackedContainer) -> None:
    """The julia (IJulia) kernel should be registered"""
    check_kernelspecs(container, ["julia"])
