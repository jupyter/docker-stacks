# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from dataclasses import dataclass, field
from typing import Optional, List
from taggers import TaggerInterface, \
    SHATagger, \
    UbuntuVersionTagger, PythonVersionTagger, \
    JupyterNotebookVersionTagger, JupyterLabVersionTagger, JupyterHubVersionTagger, \
    RVersionTagger, TensorflowVersionTagger, JuliaVersionTagger, \
    SparkVersionTagger, HadoopVersionTagger, JavaVersionTagger
from manifests import ManifestInterface, \
    BuildInfoManifest, CondaEnvironmentManifest, AptPackagesManifest


@dataclass
class ImageDescription:
    parent_image: Optional[str]
    taggers: List[TaggerInterface] = field(default_factory=list)
    manifests: List[ManifestInterface] = field(default_factory=list)


ALL_IMAGES = {
    "base-notebook": ImageDescription(
        parent_image=None,
        taggers=[
            SHATagger,
            UbuntuVersionTagger, PythonVersionTagger,
            JupyterNotebookVersionTagger, JupyterLabVersionTagger, JupyterHubVersionTagger
        ],
        manifests=[
            BuildInfoManifest, CondaEnvironmentManifest, AptPackagesManifest
        ]
    ),
    "minimal-notebook": ImageDescription(
        parent_image="base-notebook"
    ),
    "scipy-notebook": ImageDescription(
        parent_image="minimal-notebook"
    ),
    "r-notebook": ImageDescription(
        parent_image="minimal-notebook",
        taggers=[RVersionTagger]
    ),
    "tensorflow-notebook": ImageDescription(
        parent_image="scipy-notebook",
        taggers=[TensorflowVersionTagger]
    ),
    "datascience-notebook": ImageDescription(
        parent_image="scipy-notebook",
        taggers=[JuliaVersionTagger]
    ),
    "pyspark-notebook": ImageDescription(
        parent_image="scipy-notebook",
        taggers=[SparkVersionTagger, HadoopVersionTagger, JavaVersionTagger]
    ),
    "all-spark-notebook": ImageDescription(
        parent_image="pyspark-notebook",
        taggers=[RVersionTagger]
    )
}
