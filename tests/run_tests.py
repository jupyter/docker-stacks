#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import logging

import plumbum

from tests.hierarchy.get_test_dirs import get_test_dirs

python3 = plumbum.local["python3"]

LOGGER = logging.getLogger(__name__)


def test_image(*, registry: str, owner: str, image: str) -> None:
    LOGGER.info(f"Testing image: {image}")
    test_dirs = get_test_dirs(image)
    LOGGER.info(f"Test dirs to be run: {test_dirs}")
    (
        python3[
            "-m",
            "pytest",
            "--numprocesses",
            "auto",
            "-m",
            "not info",
            test_dirs,
            "--registry",
            registry,
            "--owner",
            owner,
            "--image",
            image,
        ]
        & plumbum.FG
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--registry",
        required=True,
        choices=["docker.io", "quay.io"],
        help="Image registry",
    )
    arg_parser.add_argument(
        "--owner",
        required=True,
        help="Owner of the image",
    )
    arg_parser.add_argument(
        "--image",
        required=True,
        help="Short image name",
    )
    args = arg_parser.parse_args()

    test_image(**vars(args))
