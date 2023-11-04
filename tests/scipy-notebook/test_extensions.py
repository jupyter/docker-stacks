# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

import pytest  # type: ignore

from tests.conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)


@pytest.mark.skip(reason="Not yet compliant with JupyterLab 4")
@pytest.mark.parametrize(
    "extension",
    [
        "@bokeh/jupyter_bokeh",
        "@jupyter-widgets/jupyterlab-manager",
        "jupyter-matplotlib",
    ],
)
def test_check_extension(container: TrackedContainer, extension: str) -> None:
    """Basic check of each extension

    The list of installed extensions can be obtained through this command:

    $ jupyter labextension list

    """
    LOGGER.info(f"Checking the extension: {extension} ...")
    container.run_and_wait(
        timeout=10,
        tty=True,
        command=["start.sh", "jupyter", "labextension", "check", extension],
    )
