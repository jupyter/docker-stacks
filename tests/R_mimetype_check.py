# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

from tests.conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)


def check_r_mimetypes(container: TrackedContainer) -> None:
    """Check if Rscript command can be executed"""
    LOGGER.info("Test that R command can be executed ...")
    R_MIMETYPES_CHECK_CMD = 'if (length(getOption("jupyter.plot_mimetypes")) != 5) {stop("missing jupyter.plot_mimetypes")}'
    logs = container.run_and_wait(
        timeout=10,
        tty=True,
        command=["Rscript", "-e", R_MIMETYPES_CHECK_CMD],
    )
    LOGGER.debug(f"{logs=}")
    assert len(logs) == 0, f"Command {R_MIMETYPES_CHECK_CMD=} failed"
