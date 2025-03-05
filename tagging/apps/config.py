# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    registry: str = ""
    owner: str = ""
    image: str = ""
    variant: str = ""
    platform: str = ""

    tags_dir: Path = Path()
    hist_lines_dir: Path = Path()
    manifests_dir: Path = Path()

    repository: str = ""

    def full_image(self) -> str:
        return f"{self.registry}/{self.owner}/{self.image}"
