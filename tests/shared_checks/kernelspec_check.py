# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

from tests.utils.tracked_container import TrackedContainer

LOGGER = logging.getLogger(__name__)


def check_kernelspecs(container: TrackedContainer, expected_kernels: list[str]) -> None:
    """Check that `jupyter kernelspec list` reports the expected kernels.

    A versioned kernel name (e.g. `julia-1.11`) matches
    its expected unversioned name (`julia`).
    """
    LOGGER.info(f"Checking that kernels {expected_kernels} are installed ...")
    logs = container.run_and_wait(
        timeout=30,
        command=["jupyter", "kernelspec", "list"],
    )
    # Kernels are reported as `<name> <kernel directory>` lines
    installed_kernels = {
        parts[0]
        for parts in (line.split() for line in logs.splitlines())
        if len(parts) == 2 and "/kernels/" in parts[1]
    }
    for expected_kernel in expected_kernels:
        assert any(
            kernel == expected_kernel or kernel.startswith(f"{expected_kernel}-")
            for kernel in installed_kernels
        ), f"Kernel {expected_kernel} not found in {installed_kernels}"
