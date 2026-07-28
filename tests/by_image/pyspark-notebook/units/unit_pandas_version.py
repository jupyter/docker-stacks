# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from pathlib import Path

import pandas

expected_version = Path("/opt/setup-scripts/pandas-version.txt").read_text().strip()
assert (
    pandas.__version__ == expected_version
), f"Installed pandas {pandas.__version__} != resolved {expected_version}"
