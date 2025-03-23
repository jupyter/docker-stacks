# Tags and manifests

The main purpose of the source code in [the `tagging` folder](https://github.com/jupyter/docker-stacks/tree/main/tagging) is to
properly write tags file, build history line and manifest for a single-platform image,
apply these tags, and then merge single-platform images into one multi-arch image.

## What is a tag and a manifest

A tag is a label attached to a Docker image identifying specific attributes or versions.
For example, an image `jupyter/base-notebook` with Python 3.10.5 will have a full image name `quay.io/jupyter/base-notebook:python-3.10.5`.
These tags are pushed to our [Quay.io registry](https://quay.io/organization/jupyter).

A manifest is a description of important image attributes written in Markdown format.
For example, we dump all `conda` packages with their versions into the manifest.

## Main principles

- All images are organized in a hierarchical tree.
  More info on [image relationships](../using/selecting.md#image-relationships).
- `TaggerInterface` and `ManifestInterface` are interfaces for functions to generate tags and manifest pieces by running commands in Docker containers.
- Tags and manifests are reevaluated for each image in the hierarchy since values may change between parent and child images.
- To tag an image and create its manifest and build history line, run `make hook/<somestack>` (e.g., `make hook/base-notebook`).

## Utils

### DockerRunner

`DockerRunner` is a helper class to easily run a docker container and execute commands inside this container:

```{literalinclude} tagging_examples/docker_runner.py
:language: py
:lines: 3-
```

### GitHelper

`GitHelper` methods are run in the current `git` repo and give the information about the last commit hash and commit message:

```{literalinclude} tagging_examples/git_helper.py
:language: py
:lines: 3-
```

The prefix of commit hash (namely, 12 letters) is used as an image tag to make it easy to inherit from a fixed version of a docker image.

## Taggers and Manifests

### Tagger

`Tagger` is a function that runs commands inside a docker container to calculate a tag for an image.

All the taggers follow `TaggerInterface`:

```{literalinclude} ../../tagging/taggers/tagger_interface.py
:language: py
:start-at: TaggerInterface
```

So, the `tagger(container)` gets a docker container as an input and returns a tag.

For example:

```{literalinclude} ../../tagging/taggers/sha.py
:language: py
:start-at: def
```

- `taggers/` subdirectory contains all taggers.
- `apps/write_tags_file.py`, `apps/apply_tags.py`, and `apps/merge_tags.py` are Python executables used to write tags for an image, apply tags from a file, and create multi-arch images.

### Manifest

All manifest functions except `build_info_manifest` follow `ManifestInterface`
and `manifest(container)` method returns a piece of the manifest.

```{literalinclude} ../../tagging/manifests/manifest_interface.py
:language: py
:start-at: ManifestInterface
```

For example:

```{literalinclude} ../../tagging/manifests/apt_packages.py
:language: py
:start-at: def
```

where:

- `quoted_output(container, cmd)` simply runs the command inside a container using `DockerRunner.exec_cmd` and wraps it to triple quotes to create a valid markdown piece.
  It also adds the command which was run to the markdown piece.
- `manifests/` subdirectory contains all the manifests.
- `apps/write_manifest.py` is a Python executable to create the build manifest and history line for an image.

## Images Hierarchy

All images' dependencies on each other and what taggers and manifests are applicable to them are defined in `hierarchy/images_hierarchy.py`.

`hierarchy/get_taggers.py` and `hierarchy/get_manifests.py` define functions to get the taggers and manifests for a specific image.
