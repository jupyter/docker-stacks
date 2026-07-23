# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from pathlib import Path

from tests.utils.tracked_container import TrackedContainer

LOGGER = logging.getLogger(__name__)
THIS_DIR = Path(__file__).parent.resolve()


def test_julia_nbconvert(container: TrackedContainer) -> None:
    """A trivial notebook should be executed through the julia (IJulia) kernel"""
    host_file = THIS_DIR / "data" / "execute_julia.ipynb"
    cont_data_file = "/home/jovyan/" + host_file.name
    output_dir = "/tmp"
    LOGGER.info(f"Test that the notebook {host_file.name} can be executed ...")

    # The IJulia kernel name is versioned (e.g. julia-1.11),
    # so we discover it at runtime instead of hardcoding a version
    kernel_discovery = (
        'jupyter kernelspec list | grep --only-matching "julia-[0-9.]*" | head -n 1'
    )
    command = (
        f"jupyter nbconvert {cont_data_file} --output-dir {output_dir} "
        "--to markdown --execute "
        "--ExecutePreprocessor.timeout=30 "
        "--ExecutePreprocessor.startup_timeout=120 "
        f'--ExecutePreprocessor.kernel_name="$({kernel_discovery})"'
    )
    logs = container.run_and_wait(
        timeout=180,  # IJulia kernel cold start can be slow
        volumes={host_file: {"bind": cont_data_file, "mode": "ro"}},
        command=["bash", "-c", command],
    )
    expected_file = f"{output_dir}/{host_file.stem}.md"
    assert expected_file in logs, f"Expected file {expected_file} not generated"
