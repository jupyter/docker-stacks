#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import logging
from dataclasses import dataclass, field
from typing import Optional, List
from taggers import TaggerInterface, \
    SHATagger, \
    PythonVersionTagger, \
    JupyterNotebookVersionTagger, JupyterLabVersionTagger, JupyterHubVersionTagger, \
    RVersionTagger, TensorflowVersionTagger, JuliaVersionTagger, \
    SparkVersionTagger, HadoopVersionTagger, JavaVersionTagger
from plumbum.cmd import docker


logger = logging.getLogger(__name__)


@dataclass
class ImageDescription:
    parent_image: Optional[str]
    taggers: List[TaggerInterface] = field(default_factory=list)


ALL_IMAGES = {
    "base-notebook": ImageDescription(
        parent_image=None,
        taggers=[
            SHATagger,
            PythonVersionTagger, JupyterNotebookVersionTagger, JupyterLabVersionTagger, JupyterHubVersionTagger
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
    "allspark-notebook": ImageDescription(
        parent_image="pyspark-notebook",
        taggers=[RVersionTagger]
    )
}


def get_all_taggers(short_image_name):
    taggers = []
    while short_image_name is not None:
        image_description = ALL_IMAGES[short_image_name]
        taggers = image_description.taggers + taggers
        short_image_name = image_description.parent_image
    return taggers


def apply_tags(short_image_name, owner):
    logger.info(f"Applying tags for image: {short_image_name}")
    taggers = get_all_taggers(short_image_name)

    for tagger in taggers:
        tagger_name = tagger.__name__
        tag_value = tagger.tag_value(short_image_name, owner)
        logger.info(f"Applying tag tagger_name: {tagger_name} tag_value: {tag_value}")
        docker["tag", f"{owner}/{short_image_name}:latest", f"{owner}/{short_image_name}:{tag_value}"]()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--short-image-name", required=True, help="Short image name to apply tags for")
    arg_parser.add_argument("--owner", required=True, help="Owner of the image")
    args = arg_parser.parse_args()

    short_image_name = args.short_image_name
    owner = args.owner

    assert short_image_name in ALL_IMAGES, f"Did not found {short_image_name} image description"

    apply_tags(short_image_name, owner)
