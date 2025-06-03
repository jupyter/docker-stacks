# Building a custom set of images

This section describes how to build a custom set of images.
It may be helpful if you need to change the Ubuntu or Python version, or to make a significant change to the build process itself.

This project only builds one set of images at a time.
If you want to use older images, [take a look here](../index.rst/#using-old-images).

## Automating your build using template cookiecutter project

If you wish to build your own image on top of one of our images and automate your build process,
please, [take a look at cookiecutter template](../contributing/stacks.md).

## Custom arguments

Our repository provides several customization points:

- `ROOT_IMAGE` (docker argument) - the parent image for `docker-stacks-foundation` image
- `PYTHON_VERSION` (docker argument) - the Python version to install in `docker-stacks-foundation` image
- `REGISTRY`, `OWNER`, `BASE_IMAGE` (docker arguments) - they allow to specify parent image for all the other images
- `REGISTRY`, `OWNER` (part of `env` in some GitHub workflows) - these allow to properly tag and refer to images during following steps:
  - [`build-test-upload`](https://github.com/jupyter/docker-stacks/blob/main/.github/workflows/docker-build-test-upload.yml)
  - [`contributed-recipes`](https://github.com/jupyter/docker-stacks/blob/main/.github/workflows/contributed-recipes.yml)
  - [`tag-push`](https://github.com/jupyter/docker-stacks/blob/main/.github/workflows/docker-tag-push.yml)

These customization points can't be changed during runtime.
Read more about [Docker build arguments](https://docs.docker.com/build/building/variables/#arg-usage-example) and [GitHub environment variables for a single workflow](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#defining-environment-variables-for-a-single-workflow).

## Building stack images with custom arguments

A selection of prebuilt images are available from [Quay.io](https://quay.io/organization/jupyter),
however, it's impossible to cater to everybody's needs.
For extensive customization with an automated build pipeline,
you may wish to create a [community-maintained stack](../contributing/stacks),
however, for minor customizations, this may be overkill.
For example, you may wish to use the same Jupyter stacks but built on a different base image,
or built with a different Python version.

To achieve this you can use [Docker Bake](https://docs.docker.com/build/bake/)
to build the stacks locally with custom arguments.

```{note}
Custom arguments may result in build errors due to incompatibility.
If so your use-case may require a fully customized stack.
```

As a basic example, if you want to build a custom image based on the `minimal-notebook` image using `Python 3.12`,
then with a Dockerfile like:

```{code-block} Dockerfile
:caption: Dockerfile

ARG BASE_IMAGE=minimal-notebook
FROM $BASE_IMAGE
...
```

Include the file below in your project:

```{literalinclude} recipe_code/docker-bake.custom-python.hcl
:force:
:language: hcl
:caption: docker-bake.hcl
```

To build this stack, in the same directory run:

```bash
docker buildx bake
```

Docker Bake then determines the correct build order from the `contexts` parameters
and builds the stack as requested.

This image can then be run the same way as any other image provided by this project, for example:

```bash
docker run -it --rm -p 8888:8888 custom-jupyter
```

or referenced in a Docker Compose file.

## Forking our repository

If for some reason, you need to change more things in our images, feel free to fork it and change it any way you want.
If your customization is easy to backport to the main repo and might be helpful for other users, feel free to create a PR.

It is almost always a great idea to keep your diff as small as possible and to merge/rebase the latest version of our repo in your project.
