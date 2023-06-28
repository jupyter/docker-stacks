# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from dataclasses import dataclass, field
from typing import Optional

from tagging.manifests import (
    AptPackagesManifest,
    CondaEnvironmentManifest,
    JuliaPackagesManifest,
    ManifestInterface,
    RPackagesManifest,
    SparkInfoManifest,
)
from tagging.taggers import (
    DateTagger,
    HadoopVersionTagger,
    JavaVersionTagger,
    JuliaVersionTagger,
    JupyterHubVersionTagger,
    JupyterLabVersionTagger,
    JupyterNotebookVersionTagger,
    PythonMajorMinorVersionTagger,
    PythonVersionTagger,
    RVersionTagger,
    SHATagger,
    SparkVersionTagger,
    TaggerInterface,
    TensorflowVersionTagger,
    UbuntuVersionTagger,
)


@dataclass
class ImageDescription:
    parent_image: Optional[str]
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
    "datascience-notebook": ImageDescription(
        parent_image="scipy-notebook",
        taggers=[RVersionTagger(), JuliaVersionTagger()],
        manifests=[RPackagesManifest(), JuliaPackagesManifest()],
    ),
    "pyspark-notebook": ImageDescription(
        parent_image="scipy-notebook",
        taggers=[SparkVersionTagger(), HadoopVersionTagger(), JavaVersionTagger()],
        manifests=[SparkInfoManifest()],
    ),
    "all-spark-notebook": ImageDescription(
        parent_image="pyspark-notebook",
        taggers=[RVersionTagger()],
        manifests=[RPackagesManifest()],
    ),
}
