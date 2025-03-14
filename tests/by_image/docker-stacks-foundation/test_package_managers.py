# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import pytest  # type: ignore

from tests.utils.run_command import run_command
from tests.utils.tracked_container import TrackedContainer


@pytest.mark.parametrize(
    "package_manager_command",
    [
        "apt --version",
        "conda --version",
        "mamba --version",
        "pip --version",
    ],
)
def test_package_manager(
    container: TrackedContainer, package_manager_command: str
) -> None:
    """Test that package managers are installed and run."""
    run_command(container, package_manager_command)
