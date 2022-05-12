# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from pathlib import Path

file = Path("/tmp/test-file.txt")
assert file.exists()
assert file.read_text() == "test-content\n"
