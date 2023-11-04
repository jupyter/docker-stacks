# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from pathlib import Path

from tests.conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)
THIS_DIR = Path(__file__).parent.resolve()


def test_run_hooks_zero_args(container: TrackedContainer) -> None:
    logs = container.run_and_wait(
        timeout=5,
        tty=True,
        no_failure=False,
        command=["bash", "-c", "source /usr/local/bin/run-hooks.sh"],
    )
    assert "Should pass exactly one directory" in logs


def test_run_hooks_two_args(container: TrackedContainer) -> None:
    logs = container.run_and_wait(
        timeout=5,
        tty=True,
        no_failure=False,
        command=[
            "bash",
            "-c",
            "source /usr/local/bin/run-hooks.sh first-arg second-arg",
        ],
    )
    assert "Should pass exactly one directory" in logs


def test_run_hooks_missing_dir(container: TrackedContainer) -> None:
    logs = container.run_and_wait(
        timeout=5,
        tty=True,
        no_failure=False,
        command=[
            "bash",
            "-c",
            "source /usr/local/bin/run-hooks.sh /tmp/missing-dir/",
        ],
    )
    assert "Directory /tmp/missing-dir/ doesn't exist or is not a directory" in logs


def test_run_hooks_dir_is_file(container: TrackedContainer) -> None:
    logs = container.run_and_wait(
        timeout=5,
        tty=True,
        no_failure=False,
        command=[
            "bash",
            "-c",
            "touch /tmp/some-file && source /usr/local/bin/run-hooks.sh /tmp/some-file",
        ],
    )
    assert "Directory /tmp/some-file doesn't exist or is not a directory" in logs


def test_run_hooks_empty_dir(container: TrackedContainer) -> None:
    container.run_and_wait(
        timeout=5,
        tty=True,
        command=[
            "bash",
            "-c",
            "mkdir /tmp/empty-dir && source /usr/local/bin/run-hooks.sh /tmp/empty-dir/",
        ],
    )


def run_source_in_dir(
    container: TrackedContainer,
    subdir: str,
    command_suffix: str = "",
    no_failure: bool = True,
) -> str:
    host_data_dir = THIS_DIR / subdir
    cont_data_dir = "/home/jovyan/data"
    # https://forums.docker.com/t/all-files-appear-as-executable-in-file-paths-using-bind-mount/99921
    # Unfortunately, Docker treats all files in mounter dir as executable files
    # So we make a copy of mounted dir inside a container
    command = (
        "cp -r /home/jovyan/data/ /home/jovyan/data-copy/ &&"
        "source /usr/local/bin/run-hooks.sh /home/jovyan/data-copy/" + command_suffix
    )
    return container.run_and_wait(
        timeout=5,
        volumes={str(host_data_dir): {"bind": cont_data_dir, "mode": "ro"}},
        tty=True,
        no_failure=no_failure,
        command=["bash", "-c", command],
    )


def test_run_hooks_executables(container: TrackedContainer) -> None:
    logs = run_source_in_dir(
        container,
        subdir="run-hooks-executables",
        command_suffix="&& echo SOME_VAR is ${SOME_VAR}",
    )

    assert "Executable python file was successfully run" in logs
    assert "Ignoring non-executable: /home/jovyan/data-copy//non_executable.py" in logs
    assert "SOME_VAR is 123" in logs


def test_run_hooks_with_failures(container: TrackedContainer) -> None:
    logs = run_source_in_dir(container, subdir="run-hooks-failures", no_failure=False)

    for file in ["a.sh", "b.py", "c.sh", "d.sh"]:
        assert f"Started: {file}" in logs

    for file in ["a.sh"]:
        assert f"Finished: {file}" in logs
    for file in ["b.py", "c.sh", "d.sh"]:
        assert f"Finished: {file}" not in logs

    for file in ["b.py", "c.sh"]:
        assert (
            f"/home/jovyan/data-copy//{file} has failed, continuing execution" in logs
        )

    assert "OTHER_VAR=456" in logs


def test_run_hooks_unset(container: TrackedContainer) -> None:
    logs = run_source_in_dir(container, subdir="run-hooks-unset")

    assert "Inside a.sh MY_VAR variable has 123 value" in logs
    assert "Inside b.sh MY_VAR variable has 123 value" in logs
    assert "Unsetting MY_VAR" in logs
    assert "Inside c.sh MY_VAR variable has  value" in logs


def test_run_hooks_change(container: TrackedContainer) -> None:
    logs = run_source_in_dir(container, subdir="run-hooks-change")

    assert "Inside a.sh MY_VAR variable has 123 value" in logs
    assert "Inside b.sh MY_VAR variable has 123 value" in logs
    assert "Changing value of MY_VAR" in logs
    assert "After change inside b.sh MY_VAR variable has 456 value" in logs
    assert "Inside c.sh MY_VAR variable has 456 value" in logs
