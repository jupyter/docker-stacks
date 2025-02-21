# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from docker.models.containers import Container

from tagging.manifests.manifest_interface import ManifestInterface
from tagging.utils.quoted_output import quoted_output


class AptPackagesManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container: Container) -> str:
        return f"""\
## Apt Packages

{quoted_output(container, "apt list --installed")}"""
