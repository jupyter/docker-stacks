# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging

from tests.conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)


def mimetypes_check(container: TrackedContainer) -> str:
    """Check if Rscript command can be executed"""
    LOGGER.info("Test that R command can be executed ...")
    Rcommand = 'if (length(getOption("jupyter.plot_mimetypes")) != 3) {stop("missing jupyter.plot_mimetypes")}'
    logs = container.run_and_wait(
        timeout=60,
        tty=True,
        command=["Rscript", "-e", Rcommand],
    )
    LOGGER.debug(f"{logs=}")
    assert len(logs) == 0, f"Command {Rcommand=} failed"

    return logs
