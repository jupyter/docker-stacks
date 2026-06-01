# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import re

from tests.utils.tracked_container import TrackedContainer


def test_log_format_includes_timestamp(container: TrackedContainer) -> None:
    """Log messages should include a timestamp and level."""
    _, stderr = container.run_and_wait(
        timeout=10,
        user="root",
        environment=["NB_USER=root", "NB_UID=0", "NB_GID=0"],
        command=["echo", "done"],
        split_stderr=True,
    )
    assert re.search(
        r"INFO\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Entered start\.sh", stderr
    )


def test_quiet_mode_suppresses_info(container: TrackedContainer) -> None:
    """JUPYTER_DOCKER_STACKS_QUIET should suppress INFO messages."""
    _, stderr = container.run_and_wait(
        timeout=10,
        user="root",
        environment=[
            "NB_USER=root",
            "NB_UID=0",
            "NB_GID=0",
            "JUPYTER_DOCKER_STACKS_QUIET=1",
        ],
        command=["echo", "done"],
        split_stderr=True,
    )
    assert "INFO[" not in stderr


def test_quiet_mode_shows_warnings(container: TrackedContainer) -> None:
    """JUPYTER_DOCKER_STACKS_QUIET should still show WARNING messages."""
    _, stderr = container.run_and_wait(
        timeout=10,
        environment=[
            "JUPYTER_DOCKER_STACKS_QUIET=1",
            "GRANT_SUDO=1",
        ],
        command=["echo", "done"],
        split_stderr=True,
        no_warnings=False,
    )
    assert "WARNING[" in stderr


def test_log_without_level_defaults_to_info(container: TrackedContainer) -> None:
    """Calling _log without a recognized level should default to INFO."""
    _, stderr = container.run_and_wait(
        timeout=10,
        user="root",
        environment=["NB_USER=root", "NB_UID=0", "NB_GID=0"],
        command=[
            "bash",
            "-c",
            'source /usr/local/bin/_docker_stacks_log.sh && _log "no level here"',
        ],
        split_stderr=True,
    )
    assert "INFO[" in stderr
    assert "no level here" in stderr
