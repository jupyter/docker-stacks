# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

from tests.utils.tracked_container import TrackedContainer

LOGGER = logging.getLogger(__name__)


def test_pandoc(container: TrackedContainer) -> None:
    """Pandoc shall be able to convert MD to HTML."""
    logs = container.run_and_wait(
        timeout=10,
        command=["bash", "-c", 'echo "**BOLD**" | pandoc'],
    )
    assert "<p><strong>BOLD</strong></p>" in logs
