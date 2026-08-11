# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

import pytest

from tests.utils.tracked_container import TrackedContainer

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "extension",
    [
        # Provided by the ipywidgets package
        "@jupyter-widgets/jupyterlab-manager",
        # Provided by the jupyterlab-git package
        "@jupyterlab/git",
        # Provided by the ipympl package
        "jupyter-matplotlib",
    ],
)
def test_check_extension(container: TrackedContainer, extension: str) -> None:
    """Check that the JupyterLab extensions shipped in the image
    are installed and enabled.

    The list of installed extensions is reported (on stderr) by:

    $ jupyter labextension list

    """
    LOGGER.info(f"Checking the extension: {extension} ...")
    _, stderr = container.run_and_wait(
        timeout=30,
        command=["jupyter", "labextension", "list"],
        split_stderr=True,
    )
    # The output is colorized even without a tty, e.g. "enabled" is printed as "\x1b[32menabled\x1b[0m"
    stderr = TrackedContainer._strip_ansi(stderr)
    extension_lines = [
        line for line in stderr.splitlines() if line.split()[:1] == [extension]
    ]
    assert extension_lines, f"Extension {extension} is not installed:\n{stderr}"
    for line in extension_lines:
        words = line.split()
        assert "enabled" in words, f"Extension {extension} is not enabled: {line}"
        assert "OK" in words, f"Extension {extension} is not OK: {line}"
