# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from docker.models.containers import Container

from tagging.manifests.manifest_interface import MarkdownPiece
from tagging.utils.quoted_output import quoted_output


def julia_packages_manifest(container: Container) -> MarkdownPiece:
    return MarkdownPiece(
        title="## Julia Packages",
        sections=[
            quoted_output(
                container, "julia -E 'using InteractiveUtils; versioninfo()'"
            ),
            quoted_output(container, "julia -E 'import Pkg; Pkg.status()'"),
        ],
    )
