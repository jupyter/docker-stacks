# Building a custom set of images

This section describes how to build a custom set of images.
It may be helpful if you need to change Ubuntu or Python version, or make a significant change to the build process itself.

## Building stack images with custom arguments

A selection of prebuilt images are available from Quay.io,
however, it's impossible to cater to everybody's needs.
For extensive customization with an automated build pipeline,
you may wish to create a [community-maintained stack](https://jupyter-docker-stacks.readthedocs.io/en/latest/contributing/stacks.html),
however, for minor customizations, this may be overkill.
For example, you may wish to use the same jupyter stacks but built on a different base image,
or build with a different Python version.

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

ARG BASE_CONTAINER=minimal-notebook
FROM $BASE_CONTAINER
...
```

Include the below file in your project:

```{literalinclude} recipe_code/docker-bake.python312.hcl
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

This image can then be run using:

```bash
docker run custom-jupyter
```

or referenced in a docker compose file.

## Forking our repository

The project tries to make it's best for users, who would like to fork the repository, and change a few things and build their set of images.

Existing customization points:

- `ROOT_CONTAINER` - a docker argument of `docker-stacks-foundation` image
- `PYTHON_VERSION` - a docker argument of `docker-stacks-foundation` image
- `REGISTRY`, `OWNER`, `BASE_CONTAINER` - docker arguments for all the other images we build
- `REGISTRY`, `OWNER` - part of `env` in most of our GitHub workflows

## Automating your build using template cookiecutter project

We have created a cookiecutter project, helping you to automate building a custom image.
Please, take a look at [the documentation](../contributing/stacks.md).
