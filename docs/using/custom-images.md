# Building a custom set of images

This section describes how to build a custom set of images.
It may be helpful if you need to change Ubuntu or Python version, or make a significant change to the build process itself.

## Automating your build using template cookiecutter project

If you wish to build your own image on top of one of our images and automate your build process,
please, [take a look at cookiecutter template](../contributing/stacks.md).

## Custom arguments

Existing customization points:

- `ROOT_CONTAINER` - a docker argument of `docker-stacks-foundation` image
- `PYTHON_VERSION` - a docker argument of `docker-stacks-foundation` image
- `REGISTRY`, `OWNER`, `BASE_CONTAINER` - docker arguments for all the other images we build
- `REGISTRY`, `OWNER` - part of `env` in most of our GitHub workflows

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

If for some reason, you need to change more things in our images, feel free to fork it and change it the way you like it.
If your customization is easy to backport to the main repo and might be helpful for other users, feel free to create a PR.
