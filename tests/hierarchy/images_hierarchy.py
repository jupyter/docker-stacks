# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Please, take a look at the hierarchy of the images here:
# https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#image-relationships
IMAGE_PARENT = {
    "docker-stacks-foundation": None,
    "base-notebook": "docker-stacks-foundation",
    "minimal-notebook": "base-notebook",
    "scipy-notebook": "minimal-notebook",
    "r-notebook": "minimal-notebook",
    "julia-notebook": "minimal-notebook",
    "tensorflow-notebook": "scipy-notebook",
    "pytorch-notebook": "scipy-notebook",
    "datascience-notebook": "scipy-notebook",
    "pyspark-notebook": "scipy-notebook",
    "all-spark-notebook": "pyspark-notebook",
}
