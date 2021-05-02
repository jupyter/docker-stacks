# Docker stacks tagging

The main purpose of the source code in this folder is to properly tag all the images and to update [build manifests](https://github.com/jupyter/docker-stacks/wiki).
These 2 processes are closely related, so the source code is reused where it seems to be possible.

Basic example of such a tag would be python version tag.
For an image `jupyter/base-notebook` with `python 3.8.8` we will create a tag `jupyter/base-notebook:python-3.8.8` and push it to Docker Hub.

Manifest is a description of the important parts of the image in a text form.
For example, we dump all the `conda` packages to see a list of available packages.

## Principles

- All the images are located in a hierarchical tree. More info on [image relationships](../docs/using/selecting.md#image-relationships).
- We have tagger and manifest classes, which can be run inside docker containers to create tags and build manifest pieces.
- These classes are inherited from the parent image to all the children images.
- Because manifests and tag might change for different images in the tree, taggers and manifests are reevaluated on each image. So, the values are not inherited.
- To run tag and manifest creation process, run `make hook/base-notebook` (or another image of your choice).

## Source code description

In this section we will briefly describe source code used in this folder and give simple examples.

### DockerRunner

`DockerRunner` is a helper class to easily run docker container and execute actions inside this container:


```python
from .docker_runner import DockerRunner

with DockerRunner("ubuntu:bionic") as container:
	DockerRunner.run_simple_command(container, cmd="env", print_result=True)
```

### GitHelper

`GitHelper` is run in the current `git` repo and gives the information about last commit hash and commit message:

```python
from .git_helper import GitHelper

print("Git hash:", GitHelper.commit_hash())
print("Git message:", GitHelper.commit_message())
```

First `12` letters of commit hash are also used as an image tag to make it easy to have fixed version of docker image.

### Tagger

`Tagger` is a class, which can be run inside docker container to calculate some tag for an image.

All the taggers are inherited from `TaggerInterface`:

```python
class TaggerInterface:
    """Common interface for all taggers"""
    @staticmethod
    def tag_value(container) -> str:
        raise NotImplementedError
```

So, `tag_value(container)` method gets a docker container as an input and returns some tag.

`SHATagger` example:

```python
class SHATagger(TaggerInterface):
    @staticmethod
    def tag_value(container):
        return GitHelper.commit_hash_tag()
```

`taggers.py` contains all the taggers.
`tag_image.py` is a python executable which is used to tag the image.

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

`markdown_piece(container)` method returns piece of markdown file to be used as a part of build manifest.

`AptPackagesManifest` example:

```python
class AptPackagesManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container) -> str:
        return "\n".join([
            "## Apt Packages",
            "",
            quoted_output(container, "apt list --installed")
        ])
```

`quoted_output` simply runs the command inside container using `DockerRunner.run_simple_command` and wraps it to triple quotes.
`manifests.py` contains all the manifests.
`create_manifests.py` is a python executable which is used to create the build manifest for an image.

### Images Hierarchy

Hierarchy of all the images, taggers and manifests is defined in `images_hierarchy.py` file.
`get_taggers_and_manifests.py` file helps to get all the taggers and manifests for a specific image.
