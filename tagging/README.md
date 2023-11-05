# Docker stacks tagging and manifest creation

The main purpose of the source code in this folder is to properly tag all the images and to update [build manifests](https://github.com/jupyter/docker-stacks/wiki).
These two processes are closely related, so the source code is widely reused.

A basic example of a tag is a `python` version tag.
For example, an image `jupyter/base-notebook` with `python 3.10.5` will have a full image name `quay.io/jupyter/base-notebook:python-3.10.5`.
This tag (and all the other tags) are pushed to Quay.io.

Manifest is a description of some important part of the image in a `markdown`.
For example, we dump all the `conda` packages, including their versions.

## Main principles

- All the images are located in a hierarchical tree.
  More info on [image relationships](../docs/using/selecting.md#image-relationships).
- We have `tagger` and `manifest` classes, which can be run inside docker containers to obtain tags and build manifest pieces.
- These classes are inherited from the parent image to all the children images.
- Because manifests and tags might change from parent to children, `taggers` and `manifests` are reevaluated on each image.
  So, the values are not inherited.
- To tag an image and create a manifest, run `make hook/base-notebook` (or another image of your choice).

## Source code description

In this section, we will briefly describe the source code in this folder and give examples of how to use it.

### DockerRunner

`DockerRunner` is a helper class to easily run a docker container and execute commands inside this container:

```python
from tagging.docker_runner import DockerRunner

with DockerRunner("ubuntu:22.04") as container:
    DockerRunner.run_simple_command(container, cmd="env", print_result=True)
```

### GitHelper

`GitHelper` methods are run in the current `git` repo and give the information about the last commit hash and commit message:

```python
from tagging.git_helper import GitHelper

print("Git hash:", GitHelper.commit_hash())
print("Git message:", GitHelper.commit_message())
```

The prefix of commit hash (namely, 12 letters) is used as an image tag to make it easy to inherit from a fixed version of a docker image.

### Tagger

`Tagger` is a class which can be run inside a docker container to calculate some tag for an image.

All the taggers are inherited from `TaggerInterface`:

```python
class TaggerInterface:
    """Common interface for all taggers"""

    @staticmethod
    def tag_value(container) -> str:
        raise NotImplementedError
```

So, the `tag_value(container)` method gets a docker container as an input and returns a tag.

`SHATagger` example:

```python
from tagging.git_helper import GitHelper
from tagging.taggers import TaggerInterface


class SHATagger(TaggerInterface):
    @staticmethod
    def tag_value(container):
        return GitHelper.commit_hash_tag()
```

- `taggers.py` contains all the taggers.
- `tag_image.py` is a python executable which is used to tag the image.

### Manifest

`ManifestHeader` is a build manifest header.
It contains information about `Build datetime`, `Docker image size` and `Git commit` info.

All the other manifest classes are inherited from `ManifestInterface`:

```python
class ManifestInterface:
    """Common interface for all manifests"""

    @staticmethod
    def markdown_piece(container) -> str:
        raise NotImplementedError
```

- `markdown_piece(container)` method returns a piece of markdown file to be used as a part of the build manifest.

`AptPackagesManifest` example:

```python
from tagging.manifests import ManifestInterface, quoted_output


class AptPackagesManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container) -> str:
        return f"""\
## Apt Packages

{quoted_output(container, "apt list --installed")}"""
```

- `quoted_output` simply runs the command inside a container using `DockerRunner.run_simple_command` and wraps it to triple quotes to create a valid markdown piece.
  It also adds the command which was run to the markdown piece.
- `manifests.py` contains all the manifests.
- `write_manifest.py` is a python executable which is used to create the build manifest and history line for an image.

### Images Hierarchy

All images' dependencies on each other and what taggers and manifest they make use of are defined in `images_hierarchy.py`.

`get_taggers_and_manifests.py` defines a helper function to get the taggers and manifests for a specific image.
