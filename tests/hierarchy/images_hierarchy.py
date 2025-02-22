# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from pathlib import Path

THIS_DIR = Path(__file__).parent.resolve()
IMAGE_SPECIFIC_TESTS_DIR = THIS_DIR.parent / "image_specific_tests"

assert IMAGE_SPECIFIC_TESTS_DIR.exists(), f"{IMAGE_SPECIFIC_TESTS_DIR} does not exist."

# Please, take a look at the hierarchy of the images here:
# https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#image-relationships
_IMAGE_PARENT = {
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


def get_test_dirs(image: str | None) -> list[Path]:
    if image is None:
        return []

    test_dirs = get_test_dirs(_IMAGE_PARENT[image])
    current_test_dir = IMAGE_SPECIFIC_TESTS_DIR / image
    assert current_test_dir.exists(), f"{current_test_dir} does not exist."
    test_dirs.append(current_test_dir)
    return test_dirs
