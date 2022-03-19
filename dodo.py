# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from subprocess import PIPE
from typing import Any, Generator, Optional

import doit
from doit import task_params
from doit.tools import CmdAction

from tagging.git_helper import GitHelper

# global doit config
DOIT_CONFIG = {"verbosity": 2, "default_tasks": ["build_docs"]}


# dependencies: input to the task execution -> keeps tracks of the state of file dependencies and saves the signature
# of them every time the tasks are run so if there are no modifications to the files the execution of the task is skipped
# (indicated by -- after running doit)
# target: output produced by the task execution

# -----------------------------------------------------------------------------
# Documentation and wiki tasks
# -----------------------------------------------------------------------------


def task_build_docs() -> dict[str, Any]:
    """Build Sphinx documentation 📝
    setting uptodate to False will force the task to run every time
    """

    return dict(
        file_dep=[*Paths.DOCS_MD, *Paths.DOCS_RST, *Paths.DOCS_PY],
        actions=[
            Utils.do(
                "sphinx-build",
                "-W",
                "--keep-going",
                "--color",
                Paths.DOCS,
                "docs/_build/",
            )
        ],
        targets=[Paths.DOCS_TARGET],
        uptodate=[False],
    )


# https://pydoit.org/task-creation.html#delayed-task-creation
@doit.create_after(executed="build_docs")
def task_docs_check_links() -> dict[str, Any]:
    """Checks for any broken links in the Sphinx documentation 🔗
    only created after the docs are built"""
    return dict(
        file_dep=[*Paths.DOCS.rglob("_build/*.html")],
        actions=[
            Utils.do(
                "sphinx-build",
                "-W",
                "--keep-going",
                "--color",
                "-b",
                "linkcheck",
                Paths.DOCS,
                "docs/_build",
            )
        ],
    )


# -----------------------------------------------------------------------------
# Docker related tasks
# -----------------------------------------------------------------------------


def task_docker_build() -> Generator[dict[str, Any], None, None]:
    """Build Docker images using the system's architecture"""
    for image in DockerConfig.ALL_IMAGES:
        image_meta = Utils.image_meta(image)

        yield dict(
            name=f"build:{image}",
            doc="Build the latest image for a stack using the system's architecture ⛏",
            actions=[
                Utils.do(
                    "echo",
                    f"::group::Build {DockerConfig.OWNER}/{image}- using system's architecture",
                ),
                Utils.do(
                    "docker",
                    "buildx",
                    "build",
                    *["-t" + tag for tag in image_meta.tags],
                    "-f",
                    image_meta.dockerfile,
                    "--build-arg",
                    "OWNER=" + DockerConfig.OWNER,
                    str(image_meta.dir),
                    "--load",
                ),
            ],
            file_dep=[str(image_meta.dockerfile)],
            uptodate=[False],
        )

        yield dict(
            name=f"build_summary:{image}",
            doc="Brief summary of the image built - defaulting to using the latest tag",
            actions=[
                ["echo", "\n \n ⚡️ Build complete, image size:"],
                Utils.do(
                    "docker", "images", image_meta.tags[0], "--format", "{{.Size}}"
                ),
                Utils.do("echo", "::endgroup::"),
            ],
        )


def task_docker_save_images() -> Optional[dict[str, Any]]:
    """Save the built Docker images - these will be stored as CI artifacts.
    This is needed to pass images across jobs in GitHub Actions as each job runs in a separate container."""

    if Utils.IS_CI:
        images_ids = Utils.get_images()

        return dict(
            targets=[Utils.CI_IMAGE_TAR],
            actions=[
                Utils.do("echo", f"Saving images to: {Paths.CI_IMG}"),
                Utils.do("mkdir", "-p", Paths.CI_IMG),
                Utils.do(
                    "docker",
                    "save",
                    *images_ids,
                    "-o",
                    Utils.CI_IMAGE_TAR,
                ),
            ],
        )
    return None


def task_docker_test() -> Generator[dict[str, Any], None, None]:
    """Test Docker images - needs to be run after `docker_build`"""

    if Utils.IS_CI & Path(Utils.CI_IMAGE_TAR).exists():
        """Since we are running in a CI environment and within a separate job than the one where the images are built,
        we need to load the images from the CI_IMAGE_TAR"""

        yield dict(
            name="load_images",
            doc="Load and inspect Docker images",
            actions=[
                Utils.do("docker", "load", "--input", Utils.CI_IMAGE_TAR),
                (Utils.inspect_image, [Utils.get_images()[-1]]),
                Utils.do("docker", "images"),
            ],
        )

    for image in DockerConfig.ALL_IMAGES:
        yield dict(
            name=f"test:{image}",
            doc="Run the test suite for the images - will always run the tests if an image is built",
            uptodate=[False],
            actions=[
                Utils.do(
                    Paths.TESTS_RUN,
                    "--short-image-name",
                    image,
                    "--owner",
                    DockerConfig.OWNER,
                )
            ],
        )


def task_docker_create_manifest() -> Generator[dict[str, Any], None, None]:
    """Build the manifest file and tags for the Docker images 🏷 - can be run in parallel to the build stage"""
    for image in DockerConfig.ALL_IMAGES:

        yield dict(
            name=f"tags:{image}",
            doc="Create tags for the images",
            actions=[
                Utils.do(
                    *Utils.PYM,
                    "tagging.tag_image",
                    "--short-image-name",
                    image,
                    "--owner",
                    DockerConfig.OWNER,
                ),
            ],
        )

        yield dict(
            name=f"manifest:{image}",
            doc="Create the manifest file for the images",
            targets=[Paths.WIKI_MANIFEST / f"{image}-{Utils.GIT_COMMIT_HASH_TAG}.md"],
            actions=[
                Utils.do(
                    *Utils.PYM,
                    "tagging.create_manifests",
                    "--short-image-name",
                    image,
                    "--owner",
                    DockerConfig.OWNER,
                    "--wiki-path",
                    Paths.WIKI,
                )
            ],
        )


@task_params(
    [
        dict(
            name="registry",
            short="r",
            long="registry",
            default="dockerhub",
            type=str,
        )
    ]
)
def task_docker_push_image(registry: str) -> Generator[dict[str, Any], None, None]:
    """Push all tags for a Jupyter image - only should be done after they have been tested"""
    for image in DockerConfig.ALL_IMAGES:
        yield dict(
            name=f"push:{image}",
            doc="Push the image to the specified registry",
            actions=[
                Utils.do(
                    "echo",
                    f"::group::Push {Utils.registry_image(registry, image)} system's architecture",
                ),
                Utils.do(
                    "docker",
                    "push",
                    "--all-tags",
                    f"{Utils.registry_image(registry, image)}",
                ),
                Utils.do("echo", "::endgroup::"),
            ],
        )


# -----------------------------------------------------------------------------
# Support classes and methods
# -----------------------------------------------------------------------------


class Paths:
    """Paths to project files and directories, used to provide consistency across the multiple doit tasks"""

    DODO = Path(__file__)
    ROOT = DODO.parent

    # docs
    DOCS = ROOT / "docs"
    DOCS_TARGET = ROOT / "docs/_build/html"
    README = ROOT / "README.md"
    DOCS_PY = sorted(DOCS.rglob("*.py"))
    DOCS_RST = sorted(DOCS.rglob("*.rst"))
    DOCS_SRC_MD = sorted(DOCS.rglob("*.md"))
    DOCS_MD = sorted([*DOCS_SRC_MD, README])

    # wiki
    WIKI = ROOT.parent / "wiki"
    WIKI_MANIFEST = WIKI / "manifests"

    # tests
    TESTS = ROOT / "tests"
    TESTS_RUN = TESTS / "run_tests.py"

    # CI
    CI = ROOT / ".github"
    CI_IMG = CI / "built-docker-images"


class DockerConfig:
    """Configuration of images"""

    # Docker-related
    OWNER = "jupyter"
    DOCKER_REGISTRY = "dockerhub"

    # Images supporting the following architectures:
    # - linux/amd64
    # - linux/arm64
    MULTI_IMAGES = [
        "base-notebook",
        "minimal-notebook",
        "scipy-notebook",
        "r-notebook",
        "pyspark-notebook",
        "all-spark-notebook",
    ]

    # TODO: uncomment after initial tests
    # ALL_IMAGES = [
    #     "base-notebook",
    #     "minimal-notebook",
    #     "scipy-notebook",
    #     "r-notebook",
    #     "tensorflow-notebook",
    #     "datascience-notebook",
    #     "pyspark-notebook",
    #     "all-spark-notebook",
    # ]
    ALL_IMAGES = [
        "base-notebook",
        "minimal-notebook",
    ]

    AMD64_IMAGES = ["datascience-notebook", "tensorflow-notebook"]


@dataclass
class ImageMeta:
    tags: list[str]
    dir: Path
    dockerfile: Path


class Utils:
    """Supporting methods and variables"""

    # CI specific
    IS_CI = bool(os.environ.get("CI", 0))

    # args
    PYM = ["python3", "-m"]

    # git specific - used for tagging
    SOURCE_DATE_EPOCH = GitHelper.commit_timestamp()
    GIT_COMMIT_SHA = GitHelper.short_commit_hash()
    GIT_COMMIT_HASH_TAG = GitHelper.commit_hash_tag()

    # tar file to store the images in
    CI_IMAGE_TAR = str(Paths.CI_IMG / f"docker-images-{GIT_COMMIT_SHA}.tar")

    # utility methods
    @staticmethod
    def do(*args: Any, cwd: Path = Paths.ROOT) -> CmdAction:
        """wrap a CmdAction for consistency across OS"""
        return CmdAction(list(map(str, args)), shell=False, cwd=cwd)

    @staticmethod
    def image_meta(image: str) -> ImageMeta:
        """Get the image tags and other supporting meta for building, testing and tagging"""
        tags = [
            f"{DockerConfig.OWNER}/{image}:latest",
            f"{DockerConfig.OWNER}/{image}:{Utils.GIT_COMMIT_SHA}_{Utils.SOURCE_DATE_EPOCH}",
        ]
        dir = Paths.ROOT / image
        return ImageMeta(tags=tags, dir=dir, dockerfile=dir / "Dockerfile")

    @staticmethod
    def inspect_image(image: str) -> None:
        """Since we are sharing artifacts across jobs we need to make sure that these are loaded properly.
        The easies way to check this is to run `docker inspect` on the image"""
        try:
            subprocess.check_call(
                ["docker", "image", "inspect", image], stdout=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            print(f"Image not found: {image}")

    @staticmethod
    def get_images() -> list[str]:
        """
        Since we are sharing artifacts across jobs we need to make sure that these are loaded properly.
        Here we get all the images present in the local system
        """

        images_ids = (
            subprocess.run(["docker", "images", "-q"], stdout=PIPE)
            .stdout.decode("utf-8")
            .splitlines()
        )
        return images_ids

    @staticmethod
    def registry_image(registry: str, image: str) -> str:
        """In CI we want to push images to GHCR and DockerHub in different steps
        so we need to ensure we pass the correct registry"""

        return (
            f"{registry}/{DockerConfig.OWNER}/{image}"
            if registry != DockerConfig.DOCKER_REGISTRY
            else f"{DockerConfig.OWNER}/{image}"
        )
