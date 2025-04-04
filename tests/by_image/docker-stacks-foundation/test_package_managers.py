# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import pytest  # type: ignore

from tests.utils.tracked_container import TrackedContainer


@pytest.mark.parametrize(
    "package_manager_command",
    ["apt", "conda", "mamba", "pip"],
)
def test_package_manager(
    container: TrackedContainer, package_manager_command: str
) -> None:
    """Test that package managers are installed and run."""
    container.run_and_wait(timeout=10, command=[package_manager_command, "--version"])
