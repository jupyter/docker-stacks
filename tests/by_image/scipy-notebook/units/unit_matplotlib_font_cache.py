# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from pathlib import Path

cache_dir = Path.home() / ".cache" / "matplotlib"
fontlist_files = list(cache_dir.glob("fontlist-*.json"))
assert fontlist_files, f"matplotlib font cache is not populated in {cache_dir}"
