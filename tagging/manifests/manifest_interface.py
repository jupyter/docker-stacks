# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from dataclasses import dataclass

from docker.models.containers import Container


@dataclass(frozen=True)
class MarkdownPiece:
    title: str
    sections: list[str]

    def __post_init__(self) -> None:
        # All pieces are H2
        assert self.title.startswith("## ")

    def get_str(self) -> str:
        return "\n\n".join([self.title, *self.sections])


class ManifestInterface:
    """Common interface for all manifests"""

    @staticmethod
    def markdown_piece(container: Container) -> MarkdownPiece:
        raise NotImplementedError
