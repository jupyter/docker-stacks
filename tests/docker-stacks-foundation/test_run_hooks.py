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


def test_run_hooks_with_files(container: TrackedContainer) -> None:
    host_data_dir = THIS_DIR / "run-hooks-data"
    cont_data_dir = "/home/jovyan/data"
    # https://forums.docker.com/t/all-files-appear-as-executable-in-file-paths-using-bind-mount/99921
    # Unfortunately, Docker treats all files in mounter dir as executable files
    # So we make a copy of mounted dir inside a container
    command = (
        "cp -r /home/jovyan/data/ /home/jovyan/data-copy/ &&"
        "source /usr/local/bin/run-hooks.sh /home/jovyan/data-copy/ &&"
        "echo SOME_VAR is ${SOME_VAR}"
    )
    logs = container.run_and_wait(
        timeout=5,
        volumes={str(host_data_dir): {"bind": cont_data_dir, "mode": "ro"}},
        tty=True,
        command=["bash", "-c", command],
    )
    assert "Executable python file was successfully" in logs
    assert "Ignoring non-executable: /home/jovyan/data-copy//non_executable.py" in logs
    assert "SOME_VAR is 123" in logs


def test_run_hooks_with_failures(container: TrackedContainer) -> None:
    host_data_dir = THIS_DIR / "run-hooks-failures"
    cont_data_dir = "/home/jovyan/data"
    # https://forums.docker.com/t/all-files-appear-as-executable-in-file-paths-using-bind-mount/99921
    # Unfortunately, Docker treats all files in mounter dir as executable files
    # So we make a copy of mounted dir inside a container
    command = (
        "cp -r /home/jovyan/data/ /home/jovyan/data-copy/ &&"
        "source /usr/local/bin/run-hooks.sh /home/jovyan/data-copy/"
    )
    logs = container.run_and_wait(
        timeout=5,
        volumes={str(host_data_dir): {"bind": cont_data_dir, "mode": "ro"}},
        tty=True,
        no_failure=False,
        command=["bash", "-c", command],
    )

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
