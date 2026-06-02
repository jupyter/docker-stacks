# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import re

from tests.utils.tracked_container import TrackedContainer

# Standard env vars used across these tests to run as the root user
ROOT_ENV = ["NB_USER=root", "NB_UID=0", "NB_GID=0"]

# Trivial commands used to trigger start.sh hooks
DONE_CMD = ["echo", "done"]

# Source the logging script and run an ad-hoc _log invocation
SOURCE_LOG = "source /usr/local/bin/_docker_stacks_log.sh"

# Log level prefixes (timestamp follows in square brackets)
INFO_PREFIX = "INFO["
WARNING_PREFIX = "WARNING["
ERROR_PREFIX = "ERROR["

# ANSI color sequences
ANSI_RED = "\x1b[0;31m"
ANSI_RESET = "\x1b[0m"
ANSI_PREFIX = "\x1b["

# Sample messages
TEST_ERROR_MSG = "test error"
NO_LEVEL_MSG = "no level here"

# Regex matching the exact log line emitted at the top of start.sh
START_SH_LOG_RE = re.compile(
    rf"{re.escape(INFO_PREFIX)}\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}}\] Entered start\.sh"
)


def test_log_format_includes_timestamp(container: TrackedContainer) -> None:
    """Log messages should include a timestamp and level."""
    _, stderr = container.run_and_wait(
        timeout=10,
        user="root",
        environment=ROOT_ENV,
        command=DONE_CMD,
        split_stderr=True,
    )
    assert START_SH_LOG_RE.search(stderr)


def test_quiet_mode_suppresses_info(container: TrackedContainer) -> None:
    """JUPYTER_DOCKER_STACKS_QUIET should suppress INFO messages."""
    _, stderr = container.run_and_wait(
        timeout=10,
        user="root",
        environment=[*ROOT_ENV, "JUPYTER_DOCKER_STACKS_QUIET=1"],
        command=DONE_CMD,
        split_stderr=True,
    )
    assert INFO_PREFIX not in stderr


def test_quiet_mode_shows_warnings(container: TrackedContainer) -> None:
    """JUPYTER_DOCKER_STACKS_QUIET should still show WARNING messages."""
    _, stderr = container.run_and_wait(
        timeout=10,
        environment=["JUPYTER_DOCKER_STACKS_QUIET=1", "GRANT_SUDO=1"],
        command=DONE_CMD,
        split_stderr=True,
        no_warnings=False,
    )
    assert WARNING_PREFIX in stderr


def test_log_without_level_defaults_to_info(container: TrackedContainer) -> None:
    """Calling _log without a recognized level should default to INFO."""
    _, stderr = container.run_and_wait(
        timeout=10,
        user="root",
        environment=ROOT_ENV,
        command=["bash", "-c", f'{SOURCE_LOG} && _log "{NO_LEVEL_MSG}"'],
        split_stderr=True,
    )
    assert INFO_PREFIX in stderr
    assert NO_LEVEL_MSG in stderr


def test_log_color_on_tty(container: TrackedContainer) -> None:
    """When stderr is a tty, ERROR messages should be colorized."""
    logs = container.run_and_wait(
        timeout=10,
        no_errors=False,
        user="root",
        environment=ROOT_ENV,
        command=["bash", "-c", f'{SOURCE_LOG} && _log_error "{TEST_ERROR_MSG}"'],
    )
    assert ANSI_RED in logs
    assert ERROR_PREFIX in logs
    assert TEST_ERROR_MSG in logs
    assert ANSI_RESET in logs


def test_log_no_color_without_tty(container: TrackedContainer) -> None:
    """When stderr is not a tty (split_stderr uses pipes), no ANSI codes should appear."""
    _, stderr = container.run_and_wait(
        timeout=10,
        no_errors=False,
        user="root",
        environment=ROOT_ENV,
        command=["bash", "-c", f'{SOURCE_LOG} && _log_error "{TEST_ERROR_MSG}"'],
        split_stderr=True,
    )
    assert ANSI_PREFIX not in stderr
    assert ERROR_PREFIX in stderr
    assert TEST_ERROR_MSG in stderr


def test_log_no_color_env_override(container: TrackedContainer) -> None:
    """NO_COLOR should suppress ANSI colors even when stderr is a tty."""
    logs = container.run_and_wait(
        timeout=10,
        no_errors=False,
        user="root",
        environment=[*ROOT_ENV, "NO_COLOR=1"],
        command=["bash", "-c", f'{SOURCE_LOG} && _log_error "{TEST_ERROR_MSG}"'],
    )
    assert ANSI_PREFIX not in logs
    assert ERROR_PREFIX in logs
