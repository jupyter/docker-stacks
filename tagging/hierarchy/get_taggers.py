# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from tagging.hierarchy.images_hierarchy import ALL_IMAGES
from tagging.taggers.tagger_interface import TaggerInterface


def get_taggers(image: str | None) -> list[TaggerInterface]:
    if image is None:
        return []
    image_description = ALL_IMAGES[image]
    parent_taggers = get_taggers(image_description.parent_image)
    return parent_taggers + image_description.taggers
