# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from pathlib import Path
from typing import Optional

THIS_DIR = Path(__file__).parent.resolve()

# Please, take a look at the hierarchy of the images here:
# https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#image-relationships
ALL_IMAGES = {
    "docker-stacks-foundation": None,
    "base-notebook": "docker-stacks-foundation",
    "minimal-notebook": "base-notebook",
    "scipy-notebook": "minimal-notebook",
    "r-notebook": "minimal-notebook",
    "julia-notebook": "minimal-notebook",
    "tensorflow-notebook": "scipy-notebook",
    "datascience-notebook": "scipy-notebook",
    "pyspark-notebook": "scipy-notebook",
    "all-spark-notebook": "pyspark-notebook",
}


def get_test_dirs(
    short_image_name: Optional[str],
) -> list[Path]:
    if short_image_name is None:
        return []

    test_dirs = get_test_dirs(ALL_IMAGES[short_image_name])
    if (current_image_tests_dir := THIS_DIR / short_image_name).exists():
        test_dirs.append(current_image_tests_dir)
    return test_dirs
