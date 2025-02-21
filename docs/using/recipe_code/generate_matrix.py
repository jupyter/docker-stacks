#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import json
from pathlib import Path

THIS_DIR = Path(__file__).parent.resolve()

RUNS_ON = ["ubuntu-24.04", "ubuntu-24.04-arm"]
ARM_INCOMPATIBLE_IMAGES = {"oracledb.dockerfile"}
BASE_IMAGE_PREFIX = "ARG BASE_IMAGE="


def extract_base_image(dockerfile: Path) -> str:
    """Extract base image from dockerfile"""
    for line in dockerfile.read_text().splitlines():
        if line.startswith(BASE_IMAGE_PREFIX):
            full_image = line[len(BASE_IMAGE_PREFIX) :]
            image_name = full_image[full_image.rfind("/") + 1 :]
            return "" if ":" in image_name else image_name
    raise RuntimeError(f"Base image not found in {dockerfile}")


def get_platform(runs_on: str) -> str:
    """Get platform architecture based on runner"""
    return "x86_64" if runs_on == "ubuntu-24.04" else "aarch64"


def generate_matrix() -> dict[str, list[dict[str, str]]]:
    """Generate build matrix for GitHub Actions"""
    dockerfiles = sorted(THIS_DIR.glob("*.dockerfile"))
    configurations: list[dict[str, str]] = []

    for dockerfile in dockerfiles:
        dockerfile_name = dockerfile.name

        for run in RUNS_ON:
            # Skip ARM builds for incompatible images
            if dockerfile_name in ARM_INCOMPATIBLE_IMAGES and run == "ubuntu-24.04-arm":
                continue

            configurations.append(
                {
                    "dockerfile": dockerfile_name,
                    "runs-on": run,
                    "platform": get_platform(run),
                    "parent-image": extract_base_image(dockerfile),
                }
            )

    return {"include": configurations}


if __name__ == "__main__":
    print(f"matrix={json.dumps(generate_matrix())}")
