from docker.models.containers import Container


class ManifestInterface:
    """Common interface for all manifests"""

    @staticmethod
    def markdown_piece(container: Container) -> str:
        raise NotImplementedError
