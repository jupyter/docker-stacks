#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
import os

import plumbum
from tenacity import (  # type: ignore
    RetryError,
    retry,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from tagging.apps.common_cli_arguments import common_arguments_parser
from tagging.apps.config import Config
from tagging.utils.get_platform import ALL_PLATFORMS
from tagging.utils.get_prefix import get_file_prefix_for_platform
from tagging.utils.git_helper import GitHelper

docker = plumbum.local["docker"]

LOGGER = logging.getLogger(__name__)

MANIFEST_NOT_FOUND_ERRORS = ("manifest unknown", "name unknown", "not found")


class ManifestNotFoundError(RuntimeError):
    """Raised when the registry definitively reports that a manifest doesn't exist"""


def read_local_tags_from_files(config: Config) -> dict[str, set[str]]:
    LOGGER.info(f"Read tags from file(s) for image: {config.image}")

    local_platforms_per_tag: dict[str, set[str]] = {}
    for platform in ALL_PLATFORMS:
        LOGGER.info(f"Reading tags for platform: {platform}")

        file_prefix = get_file_prefix_for_platform(
            platform=platform, variant=config.variant
        )
        filename = f"{file_prefix}-{config.image}.txt"
        path = config.tags_dir / filename
        if not path.exists():
            LOGGER.info(f"Tag file: {path} doesn't exist")
            continue

        LOGGER.info(f"Tag file: {path} found")
        for tag in path.read_text().splitlines():
            merged_tag = tag.replace(platform + "-", "")
            local_platforms_per_tag.setdefault(merged_tag, set()).add(platform)

    LOGGER.info(f"Tags read for image: {config.image}")
    return local_platforms_per_tag


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4),
    # A definitive answer from the registry that the manifest doesn't exist
    # is not a transient error, so there is no reason to retry
    retry=retry_if_not_exception_type(ManifestNotFoundError),
)
def inspect_manifest(tag: str) -> None:
    LOGGER.info(f"Inspecting manifest for tag: {tag}")
    retcode, stdout, stderr = docker["buildx", "imagetools", "inspect", tag].run(
        retcode=None
    )
    if retcode == 0:
        LOGGER.info(f"Manifest {tag} exists")
        return
    output = f"{stdout}\n{stderr}"
    if any(error in output.lower() for error in MANIFEST_NOT_FOUND_ERRORS):
        raise ManifestNotFoundError(
            f"Manifest for tag: {tag} doesn't exist in the registry:\n{output}"
        )
    raise RuntimeError(f"Failed to inspect manifest for tag: {tag}\n{output}")


def find_platform_tags(
    merged_tag: str, local_platforms: set[str], push_to_registry: bool
) -> list[str]:
    platform_tags = []

    for platform in sorted(local_platforms):
        platform_tag = merged_tag.replace(":", f":{platform}-")
        LOGGER.info(f"Trying to inspect: {platform_tag} in the registry")
        try:
            inspect_manifest(platform_tag)
            platform_tags.append(platform_tag)
            LOGGER.info(f"Tag {platform_tag} found successfully")
        except ManifestNotFoundError as e:
            if push_to_registry:
                raise RuntimeError(
                    f"Tag: {platform_tag} is declared in a local tags file, "
                    f"but doesn't exist in the registry. "
                    f"Merging tag: {merged_tag} would silently drop this platform."
                ) from e
            LOGGER.warning(f"Manifest for tag {platform_tag} doesn't exist")
        except RetryError as e:
            if push_to_registry:
                raise RuntimeError(
                    f"Failed to inspect manifest for tag: {platform_tag}. "
                    f"Not merging tag: {merged_tag} "
                    f"to avoid pushing an incomplete manifest list."
                ) from e
            LOGGER.warning(f"Failed to inspect manifest for tag {platform_tag}")

    return platform_tags


def merge_tags(
    merged_tag: str, local_platforms: set[str], push_to_registry: bool
) -> None:
    LOGGER.info(f"Trying to merge tag: {merged_tag}")

    # Commit SHA tags are only pushed to the registry from the default branch,
    # so there is no reason to spend time inspecting them in dry-run mode
    if not push_to_registry and merged_tag.endswith(GitHelper.commit_hash_tag()):
        LOGGER.info(
            f"Not running merge for tag: {merged_tag} "
            "as it's a commit SHA tag and it wasn't pushed to registry"
        )
        return

    platform_tags = find_platform_tags(merged_tag, local_platforms, push_to_registry)
    if not platform_tags:
        if push_to_registry:
            raise RuntimeError(
                f"No platform tags found for merged tag: {merged_tag}, "
                "and push to registry is enabled. "
                "Cannot create a manifest for a non-existing image."
            )
        LOGGER.info(
            f"Not running merge for tag: {merged_tag} as no platform tags found"
        )
        return

    args = [
        "buildx",
        "imagetools",
        "create",
        *platform_tags,
        "--tag",
        merged_tag,
    ]
    if not push_to_registry:
        args.append("--dry-run")

    LOGGER.info(f"Running command: {' '.join(args)}")
    docker[args] & plumbum.FG
    if push_to_registry:
        LOGGER.info(f"Pushed merged tag: {merged_tag}")
    else:
        LOGGER.info(f"Skipped push for tag: {merged_tag}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    config = common_arguments_parser(image=True, variant=True, tags_dir=True)
    push_to_registry = os.environ.get("PUSH_TO_REGISTRY", "false").lower() == "true"

    LOGGER.info(f"Merging tags for image: {config.image}")

    local_platforms_per_tag = read_local_tags_from_files(config)
    for tag, local_platforms in local_platforms_per_tag.items():
        merge_tags(tag, local_platforms, push_to_registry)

    LOGGER.info(f"Successfully merged tags for image: {config.image}")
