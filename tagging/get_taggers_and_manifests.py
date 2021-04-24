# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from images_hierarchy import ALL_IMAGES


def get_taggers_and_manifests(short_image_name):
    taggers = []
    manifests = []
    while short_image_name is not None:
        image_description = ALL_IMAGES[short_image_name]

        taggers = image_description.taggers + taggers
        manifests = image_description.manifests + manifests

        short_image_name = image_description.parent_image
    return taggers, manifests
