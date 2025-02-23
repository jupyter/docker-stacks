# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from docker.models.containers import Container

from tagging.manifests.manifest_interface import ManifestInterface, MarkdownPiece
from tagging.utils.quoted_output import quoted_output


class RPackagesManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container: Container) -> MarkdownPiece:
        return MarkdownPiece(
            title="## R Packages",
            sections=[
                quoted_output(container, "R --version"),
                quoted_output(
                    container, "R --silent -e 'installed.packages(.Library)[, c(1,3)]'"
                ),
            ],
        )
