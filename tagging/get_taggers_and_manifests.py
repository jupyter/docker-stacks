# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from typing import List, Tuple
from .images_hierarchy import ALL_IMAGES
from .manifests import ManifestInterface
from .taggers import TaggerInterface


def get_taggers_and_manifests(
    short_image_name: str,
) -> Tuple[List[TaggerInterface], List[ManifestInterface]]:
    taggers: List[TaggerInterface] = []
    manifests: List[ManifestInterface] = []
    while short_image_name is not None:
        image_description = ALL_IMAGES[short_image_name]

        taggers = image_description.taggers + taggers
        manifests = image_description.manifests + manifests

        short_image_name = image_description.parent_image
    return taggers, manifests
