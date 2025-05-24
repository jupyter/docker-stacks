# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from pathlib import Path

from tests.utils.tracked_container import TrackedContainer

LOGGER = logging.getLogger(__name__)


def check_nbconvert(
    container: TrackedContainer,
    host_file: Path,
    output_format: str,
    *,
    execute: bool,
    no_warnings: bool = True,
) -> str:
    """Check if nbconvert is able to convert a notebook file"""
    cont_data_file = "/home/jovyan/" + host_file.name

    output_dir = "/tmp"
    LOGGER.info(
        f"Test that the example notebook {host_file.name} can be converted to {output_format} ..."
    )
    command = [
        "jupyter",
        "nbconvert",
        cont_data_file,
        "--output-dir",
        output_dir,
        "--to",
        output_format,
    ]
    if execute:
        conversion_timeout_ms = 5000
        command += [
            "--execute",
            f"--ExecutePreprocessor.timeout={conversion_timeout_ms}",
        ]
    logs = container.run_and_wait(
        timeout=60,
        volumes={host_file: {"bind": cont_data_file, "mode": "ro"}},
        command=command,
        no_warnings=no_warnings,
    )
    output_ext = "md" if output_format == "markdown" else output_format
    expected_file = f"{output_dir}/{host_file.stem}.{output_ext}"
    assert expected_file in logs, f"Expected file {expected_file} not generated"

    return logs
