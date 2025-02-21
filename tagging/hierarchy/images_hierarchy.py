# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from dataclasses import dataclass, field

from tagging.manifests.apt_packages import AptPackagesManifest
from tagging.manifests.conda_environment import CondaEnvironmentManifest
from tagging.manifests.julia_packages import JuliaPackagesManifest
from tagging.manifests.manifest_interface import ManifestInterface
from tagging.manifests.r_packages import RPackagesManifest
from tagging.manifests.spark_info import SparkInfoManifest
from tagging.taggers.date import DateTagger
from tagging.taggers.sha import SHATagger
from tagging.taggers.tagger_interface import TaggerInterface
from tagging.taggers.ubuntu_version import UbuntuVersionTagger
from tagging.taggers.versions import (
    JavaVersionTagger,
    JuliaVersionTagger,
    JupyterHubVersionTagger,
    JupyterLabVersionTagger,
    JupyterNotebookVersionTagger,
    PythonMajorMinorVersionTagger,
    PythonVersionTagger,
    PytorchVersionTagger,
    RVersionTagger,
    SparkVersionTagger,
    TensorflowVersionTagger,
)


@dataclass
class ImageDescription:
    parent_image: str | None
    taggers: list[TaggerInterface] = field(default_factory=list)
    manifests: list[ManifestInterface] = field(default_factory=list)


ALL_IMAGES = {
    "docker-stacks-foundation": ImageDescription(
        parent_image=None,
        taggers=[
            SHATagger(),
            DateTagger(),
            UbuntuVersionTagger(),
            PythonMajorMinorVersionTagger(),
            PythonVersionTagger(),
        ],
        manifests=[CondaEnvironmentManifest(), AptPackagesManifest()],
    ),
    "base-notebook": ImageDescription(
        parent_image="docker-stacks-foundation",
        taggers=[
            JupyterNotebookVersionTagger(),
            JupyterLabVersionTagger(),
            JupyterHubVersionTagger(),
        ],
    ),
    "minimal-notebook": ImageDescription(parent_image="base-notebook"),
    "scipy-notebook": ImageDescription(parent_image="minimal-notebook"),
    "r-notebook": ImageDescription(
        parent_image="minimal-notebook",
        taggers=[RVersionTagger()],
        manifests=[RPackagesManifest()],
    ),
    "julia-notebook": ImageDescription(
        parent_image="minimal-notebook",
        taggers=[JuliaVersionTagger()],
        manifests=[JuliaPackagesManifest()],
    ),
    "tensorflow-notebook": ImageDescription(
        parent_image="scipy-notebook", taggers=[TensorflowVersionTagger()]
    ),
    "pytorch-notebook": ImageDescription(
        parent_image="scipy-notebook", taggers=[PytorchVersionTagger()]
    ),
    "datascience-notebook": ImageDescription(
        parent_image="scipy-notebook",
        taggers=[RVersionTagger(), JuliaVersionTagger()],
        manifests=[RPackagesManifest(), JuliaPackagesManifest()],
    ),
    "pyspark-notebook": ImageDescription(
        parent_image="scipy-notebook",
        taggers=[SparkVersionTagger(), JavaVersionTagger()],
        manifests=[SparkInfoManifest()],
    ),
    "all-spark-notebook": ImageDescription(
        parent_image="pyspark-notebook",
        taggers=[RVersionTagger()],
        manifests=[RPackagesManifest()],
    ),
}
