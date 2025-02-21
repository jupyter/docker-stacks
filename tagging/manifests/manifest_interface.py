# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from docker.models.containers import Container


class ManifestInterface:
    """Common interface for all manifests"""

    @staticmethod
    def markdown_piece(container: Container) -> str:
        raise NotImplementedError
