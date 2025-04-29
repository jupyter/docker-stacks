# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from __future__ import annotations

import logging
from pathlib import Path

from tests.utils.tracked_container import TrackedContainer

LOGGER = logging.getLogger(__name__)
THIS_DIR = Path(__file__).parent.resolve()


def test_run_hooks_zero_args(container: TrackedContainer) -> None:
    stdout, stderr = container.run_and_wait(
        timeout=10,
        no_errors=False,
        no_failure=False,
        split_stderr=True,
        command=["bash", "-c", "source /usr/local/bin/run-hooks.sh"],
    )
    assert not stdout
    assert "Should pass exactly one directory" in stderr


def test_run_hooks_two_args(container: TrackedContainer) -> None:
    stdout, stderr = container.run_and_wait(
        timeout=10,
        no_errors=False,
        no_failure=False,
        split_stderr=True,
        command=[
            "bash",
            "-c",
            "source /usr/local/bin/run-hooks.sh first-arg second-arg",
        ],
    )
    assert not stdout
    assert "Should pass exactly one directory" in stderr


def test_run_hooks_missing_dir(container: TrackedContainer) -> None:
    stdout, stderr = container.run_and_wait(
        timeout=10,
        no_errors=False,
        no_failure=False,
        split_stderr=True,
        command=[
            "bash",
            "-c",
            "source /usr/local/bin/run-hooks.sh /tmp/missing-dir/",
        ],
    )
    assert not stdout
    assert "Directory /tmp/missing-dir/ doesn't exist or is not a directory" in stderr


def test_run_hooks_dir_is_file(container: TrackedContainer) -> None:
    stdout, stderr = container.run_and_wait(
        timeout=10,
        no_errors=False,
        no_failure=False,
        split_stderr=True,
        command=[
            "bash",
            "-c",
            "touch /tmp/some-file && source /usr/local/bin/run-hooks.sh /tmp/some-file",
        ],
    )
    assert not stdout
    assert "Directory /tmp/some-file doesn't exist or is not a directory" in stderr


def test_run_hooks_empty_dir(container: TrackedContainer) -> None:
    stdout, stderr = container.run_and_wait(
        timeout=10,
        split_stderr=True,
        command=[
            "bash",
            "-c",
            "mkdir /tmp/empty-dir && source /usr/local/bin/run-hooks.sh /tmp/empty-dir/",
        ],
    )
    assert not stdout
    assert "Running hooks in: /tmp/empty-dir/" in stderr


def run_source_in_dir(
    container: TrackedContainer,
    *,
    subdir: str,
    command_suffix: str = "",
    no_errors: bool = True,
    no_failure: bool = True,
) -> tuple[str, str]:
    host_data_dir = THIS_DIR / subdir
    cont_data_dir = "/home/jovyan/data"
    # https://forums.docker.com/t/all-files-appear-as-executable-in-file-paths-using-bind-mount/99921
    # Unfortunately, Docker treats all files in mounted dir as executable files
    # So we make a copy of the mounted dir inside a container
    command = (
        "cp -r /home/jovyan/data/ /home/jovyan/data-copy/ &&"
        "source /usr/local/bin/run-hooks.sh /home/jovyan/data-copy/" + command_suffix
    )
    return container.run_and_wait(
        timeout=10,
        volumes={host_data_dir: {"bind": cont_data_dir, "mode": "ro"}},
        no_errors=no_errors,
        no_failure=no_failure,
        split_stderr=True,
        command=["bash", "-c", command],
    )


def test_run_hooks_change(container: TrackedContainer) -> None:
    stdout, logs = run_source_in_dir(container, subdir="data/run-hooks/change")

    assert "Inside a.sh MY_VAR variable has 123 value" in stdout
    assert "Inside b.sh MY_VAR variable has 123 value" in stdout
    assert "Changing value of MY_VAR" in stdout
    assert "After change inside b.sh MY_VAR variable has 456 value" in stdout
    assert "Inside c.sh MY_VAR variable has 456 value" in stdout


def test_run_hooks_executables(container: TrackedContainer) -> None:
    stdout, logs = run_source_in_dir(
        container,
        subdir="data/run-hooks/executables",
        command_suffix="&& echo SOME_VAR is ${SOME_VAR}",
    )

    assert "Executable python file was successfully run" in stdout
    assert "Ignoring non-executable: /home/jovyan/data-copy//non_executable.py" in logs
    assert "SOME_VAR is 123" in stdout


def test_run_hooks_failures(container: TrackedContainer) -> None:
    stdout, logs = run_source_in_dir(
        container,
        subdir="data/run-hooks/failures",
        no_errors=False,
        no_failure=False,
    )

    for file in ["a.sh", "b.py", "c.sh", "d.sh"]:
        assert f"Started: {file}" in stdout

    for file in ["a.sh"]:
        assert f"Finished: {file}" in stdout
    for file in ["b.py", "c.sh", "d.sh"]:
        assert f"Finished: {file}" not in stdout

    for file in ["b.py", "c.sh"]:
        assert (
            f"/home/jovyan/data-copy//{file} has failed, continuing execution" in logs
        )

    assert "OTHER_VAR=456" in stdout


def test_run_hooks_sh_files(container: TrackedContainer) -> None:
    stdout, _ = run_source_in_dir(container, subdir="data/run-hooks/sh-files")

    assert "Inside executable.sh MY_VAR variable has 0 value" in stdout
    assert "Inside non-executable.sh MY_VAR variable has 1 value" in stdout


def test_run_hooks_unset(container: TrackedContainer) -> None:
    stdout, _ = run_source_in_dir(container, subdir="data/run-hooks/unset")

    assert "Inside a.sh MY_VAR variable has 123 value" in stdout
    assert "Inside b.sh MY_VAR variable has 123 value" in stdout
    assert "Unsetting MY_VAR" in stdout
    assert "Inside c.sh MY_VAR variable has  value" in stdout
