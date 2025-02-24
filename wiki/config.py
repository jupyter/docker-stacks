# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    wiki_dir: Path
    hist_lines_dir: Path
    manifests_dir: Path

    repository: str
    allow_no_files: bool
