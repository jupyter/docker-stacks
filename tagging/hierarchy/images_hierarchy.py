# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from dataclasses import dataclass, field

from tagging.manifests.apt_packages import apt_packages_manifest
from tagging.manifests.conda_environment import conda_environment_manifest
from tagging.manifests.julia_packages import julia_packages_manifest
from tagging.manifests.manifest_interface import ManifestInterface
from tagging.manifests.r_packages import r_packages_manifest
from tagging.manifests.spark_info import spark_info_manifest
from tagging.taggers import versions
from tagging.taggers.date import date_tagger
from tagging.taggers.sha import commit_sha_tagger
from tagging.taggers.tagger_interface import TaggerInterface
from tagging.taggers.ubuntu_version import ubuntu_version_tagger


@dataclass
class ImageDescription:
    parent_image: str | None
    taggers: list[TaggerInterface] = field(default_factory=list)
    manifests: list[ManifestInterface] = field(default_factory=list)


ALL_IMAGES = {
    "docker-stacks-foundation": ImageDescription(
        parent_image=None,
        taggers=[
            commit_sha_tagger,
            date_tagger,
            ubuntu_version_tagger,
            versions.python_major_minor_tagger,
            versions.python_tagger,
            versions.mamba_tagger,
            versions.conda_tagger,
        ],
        manifests=[conda_environment_manifest, apt_packages_manifest],
    ),
    "base-notebook": ImageDescription(
        parent_image="docker-stacks-foundation",
        taggers=[
            versions.jupyter_notebook_tagger,
            versions.jupyter_lab_tagger,
            versions.jupyter_hub_tagger,
        ],
    ),
    "minimal-notebook": ImageDescription(parent_image="base-notebook"),
    "scipy-notebook": ImageDescription(parent_image="minimal-notebook"),
    "r-notebook": ImageDescription(
        parent_image="minimal-notebook",
        taggers=[versions.r_tagger],
        manifests=[r_packages_manifest],
    ),
    "julia-notebook": ImageDescription(
        parent_image="minimal-notebook",
        taggers=[versions.julia_tagger],
        manifests=[julia_packages_manifest],
    ),
    "tensorflow-notebook": ImageDescription(
        parent_image="scipy-notebook", taggers=[versions.tensorflow_tagger]
    ),
    "pytorch-notebook": ImageDescription(
        parent_image="scipy-notebook", taggers=[versions.python_tagger]
    ),
    "datascience-notebook": ImageDescription(
        parent_image="scipy-notebook",
        taggers=[versions.r_tagger, versions.julia_tagger],
        manifests=[r_packages_manifest, julia_packages_manifest],
    ),
    "pyspark-notebook": ImageDescription(
        parent_image="scipy-notebook",
        taggers=[versions.spark_tagger, versions.java_tagger],
        manifests=[spark_info_manifest],
    ),
    "all-spark-notebook": ImageDescription(
        parent_image="pyspark-notebook",
        taggers=[versions.r_tagger],
        manifests=[r_packages_manifest],
    ),
}
