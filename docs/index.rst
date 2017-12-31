Jupyter Docker Stacks
=====================

Jupyter Docker Stacks are a set of ready-to-run Docker images containing Jupyter applications and interactive computing tools. You can use a stack image to start a personal Jupyter Notebook server in a local Docker container, to run JupyterLab servers for a team using JupyterHub, to write your own project Dockerfile, and so on.

**Table of Contents**

.. toctree::
   :maxdepth: 1

   using
   features
   contributing

Quick Start
-----------

The examples below may help you get started if you have Docker installed, know which Docker image you want to use, and want to launch a single Jupyter Notebook server in a container. The other pages in this documentation describe additional uses and features in detail.::

    # Run a Jupyter Notebook server in a Docker container started
    # from the jupyter/scipy-notebook image built from Git commit 27ba573.
    # All files saved in the container are lost when the notebook server exits.
    # -ti: pseudo-TTY+STDIN open, so the logs appear in the terminal
    # -rm: remove the container on exit
    # -p: publish the notebook port 8888 as port 8888 on the host
    docker run -ti --rm -p 8888:8888 jupyter/scipy-notebook:27ba573

    # Run a Jupyter Notebook server in a Docker container started from the
    # jupyter/r-notebook image built from Git commit cf1a3aa.
    # All files written to ~/work in the container are saved to the
    # current working on the host and persist even when the notebook server
    # exits.
    docker run -ti --rm -p 8888:8888 -v "$PWD":/home/jovyan/work jupyter/r-notebook:cf1a3aa

    # Run a Jupyter Notebook server in a background Docker container started
    # from the latest jupyter/all-spark-notebook image available on the local
    # machine or Docker Cloud. All files saved in the container are lost
    # when the container is destroyed.
    # -d: detach, run container in background.
    # -P: Publish all exposed ports to random ports
    docker run -d -P jupyter/all-spark-notebook:latest
