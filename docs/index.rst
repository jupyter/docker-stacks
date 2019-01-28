Jupyter Docker Stacks
=====================

Jupyter Docker Stacks are a set of ready-to-run Docker images containing Jupyter applications and interactive computing tools. You can use a stack image to do any of the following (and more):

* Start a personal Jupyter Notebook server in a local Docker container
* Run JupyterLab servers for a team using JupyterHub
* Write your own project Dockerfile

Quick Start
-----------

You can try a `recent build of the jupyter/base-notebook image on mybinder.org <https://mybinder.org/v2/gh/jupyter/docker-stacks/master?filepath=README.ipynb>`_ by simply clicking the preceding link. Otherwise, the two examples below may help you get started if you `have Docker installed <https://docs.docker.com/install/>`_, know :doc:`which Docker image <using/selecting>` you want to use, and want to launch a single Jupyter Notebook server in a container.

The other pages in this documentation describe additional uses and features in detail.

**Example 1:** This command pulls the ``jupyter/scipy-notebook`` image tagged ``17aba6048f44`` from Docker Hub if it is not already present on the local host. It then starts a container running a Jupyter Notebook server and exposes the server on host port 8888. The server logs appear in the terminal. Visiting ``http://<hostname>:8888/?token=<token>`` in a browser loads the Jupyter Notebook dashboard page, where ``hostname`` is the name of the computer running docker and ``token`` is the secret token printed in the console. The container remains intact for restart after the notebook server exits.::

    docker run -p 8888:8888 jupyter/scipy-notebook:17aba6048f44

**Example 2:** This command performs the same operations as **Example 1**, but it exposes the server on host port 10000 instead of port 8888. Visiting ``http://<hostname>:10000/?token=<token>`` in a browser loads JupyterLab, where ``hostname`` is the name of the computer running docker and ``token`` is the secret token printed in the console.::

    docker run -p 10000:8888 jupyter/scipy-notebook:17aba6048f44

**Example 3:** This command pulls the ``jupyter/datascience-notebook`` image tagged ``9b06df75e445`` from Docker Hub if it is not already present on the local host. It then starts an *ephemeral* container running a Jupyter Notebook server and exposes the server on host port 10000. The command mounts the current working directory on the host as ``/home/jovyan/work`` in the container. The server logs appear in the terminal. Visiting ``http://<hostname>:10000/?token=<token>`` in a browser loads JupyterLab, where ``hostname`` is the name of the computer running docker and ``token`` is the secret token printed in the console. Docker destroys the container after notebook server exit, but any files written to ``~/work`` in the container remain intact on the host.::

    docker run --rm -p 10000:8888 -e JUPYTER_ENABLE_LAB=yes -v "$PWD":/home/jovyan/work jupyter/datascience-notebook:9b06df75e445

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   using/selecting
   using/running
   using/common
   using/specifics
   using/recipes

.. toctree::
   :maxdepth: 2
   :caption: Contributor Guide

   contributing/packages
   contributing/recipes
   contributing/tests
   contributing/features
   contributing/stacks

.. toctree::
   :maxdepth: 2
   :caption: Maintainer Guide

   maintaining/tasks

.. toctree::
   :maxdepth: 2
   :caption: Getting Help

   Jupyter Docker Stacks Issue Tracker <https://github.com/jupyter/docker-stacks>
   Jupyter Google Group <https://groups.google.com/forum/#!forum/jupyter>
   Jupyter Website <https://jupyter.org>
