# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging


logger = logging.getLogger(__name__)


class ManifestInterface:
    """Common interface for all manifests"""
    @staticmethod
    def manifest_piece(container):
        raise NotImplementedError


class BuildInfoManifest(ManifestInterface):
    @staticmethod
    def manifest_piece(container):
        return None


class CondaEnvironmentManifest(ManifestInterface):
    @staticmethod
    def manifest_piece(container):
        return None


class AptPackagesManifest(ManifestInterface):
    @staticmethod
    def manifest_piece(container):
        return None
