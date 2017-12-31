# Users Guide

Using one of the Jupyter Docker Stacks requires two choices:

1. Which Docker image you wish to use
2. How you wish to start Docker containers from that image

This section provides details about the available images and runtimes to inform your choices.

## Selecting an Image

### Core Stacks

The Jupyter team maintains a set of Docker image definitions in the https://github.com/jupyter/docker-stacks GitHub repository. The following table describes these images, and links to their source on GitHub and their builds on Docker Cloud.

|Name                        |Description|GitHub |Image Tags|
|----------------------------|-----------|-----------|----------|
|jupyter/base-notebook       ||||
|jupyter/minimal-notebook    ||||
|jupyter/r-notebook          ||||
|jupyter/scipy-notebook      ||||
|jupyter/datascience-notebook||||
|jupyter/tensorflow-notebook ||||
|jupyter/pyspark-notebook    ||||
|jupyter/all-spark-notebook  ||||
|----------------------------|-|-|-|

#### Image Relationships

The following diagram depicts the build dependencies between the core images (aka the `FROM` statement in their Dockerfiles). Any image lower in the tree inherits

[![Image inheritance diagram](internal/inherit-diagram.svg)](http://interactive.blockdiag.com/?compression=deflate&src=eJyFzTEPgjAQhuHdX9Gws5sQjGzujsaYKxzmQrlr2msMGv-71K0srO_3XGud9NNA8DSfgzESCFlBSdi0xkvQAKTNugw4QnL6GIU10hvX-Zh7Z24OLLq2SjaxpvP10lX35vCf6pOxELFmUbQiUz4oQhYzMc3gCrRt2cWe_FKosmSjyFHC6OS1AwdQWCtyj7sfh523_BI9hKlQ25YdOFdv5fcH0kiEMA)

#### Versioning

[Click here for a commented build history of each image, with references to tag/SHA values.](https://github.com/jupyter/docker-stacks/wiki/Docker-build-history)

The following are quick-links to READMEs about each image and their Docker image tags on Docker Cloud:

* base-notebook: [README](https://github.com/jupyter/docker-stacks/tree/master/base-notebook), [SHA list](https://hub.docker.com/r/jupyter/base-notebook/tags/)
* minimal-notebook: [README](https://github.com/jupyter/docker-stacks/tree/master/minimal-notebook), [SHA list](https://hub.docker.com/r/jupyter/minimal-notebook/tags/)
* scipy-notebook: [README](https://github.com/jupyter/docker-stacks/tree/master/scipy-notebook), [SHA list](https://hub.docker.com/r/jupyter/scipy-notebook/tags/)
* r-notebook: [README](https://github.com/jupyter/docker-stacks/tree/master/r-notebook), [SHA list](https://hub.docker.com/r/jupyter/r-notebook/tags/)
* tensorflow-notebook: [README](https://github.com/jupyter/docker-stacks/tree/master/tensorflow-notebook), [SHA list](https://hub.docker.com/r/jupyter/tensorflow-notebook/tags/)
* datascience-notebook: [README](https://github.com/jupyter/docker-stacks/tree/master/datascience-notebook), [SHA list](https://hub.docker.com/r/jupyter/datascience-notebook/tags/)
* pyspark-notebook: [README](https://github.com/jupyter/docker-stacks/tree/master/pyspark-notebook), [SHA list](https://hub.docker.com/r/jupyter/pyspark-notebook/tags/)
* all-spark-notebook: [README](https://github.com/jupyter/docker-stacks/tree/master/all-spark-notebook), [SHA list](https://hub.docker.com/r/jupyter/all-spark-notebook/tags/)


The latest tag in each Docker Hub repository tracks the master branch HEAD reference on GitHub. This is a moving target and will make backward-incompatible changes regularly.
Any 12-character image tag on Docker Hub refers to a git commit SHA here on GitHub. See the Docker build history wiki page for a table of build details.
Stack contents (e.g., new library versions) will be updated upon request via PRs against this project.
Users looking for reproducibility or stability should always refer to specific git SHA tagged images in their work, not latest.
For legacy reasons, there are two additional tags named 3.2 and 4.0 on Docker Hub which point to images prior to our versioning scheme switch.
If you haven't already, pin your image to a tag, e.g. FROM jupyter/scipy-notebook:7c45ec67c8e7. latest is a moving target which can change in backward-incompatible ways as packages and operating systems are updated.

## Community Stacks

The Jupyter community maintains additional

## Running a Container

### Using the Docker Command Line

### Using JupyterHub

Every notebook stack is compatible with JupyterHub 0.5 or higher. When running with JupyterHub, you must override the Docker run command to point to the `start-singleuser.sh script, which starts a single-user instance of the Notebook server. See each stack's README for instructions on running with JupyterHub.

### Using Binder