# Running a Container

Using one of the Jupyter Docker Stacks requires two choices:

1. Which Docker image you wish to use
2. How you wish to start Docker containers from that image

This section provides details about the second.

## Using the Docker CLI

You can launch a local Docker container from the Jupyter Docker Stacks using the [Docker command line interface](https://docs.docker.com/engine/reference/commandline/cli/). There are numerous ways to configure containers using the CLI. The following are some common patterns.

**Example 1** This command pulls the `jupyter/scipy-notebook` image tagged `2c80cf3537ca` from Docker Hub if it is not already present on the local host. It then starts a container running a Jupyter Notebook server and exposes the server on host port 8888. The server logs appear in the terminal and include a URL to the notebook server.

```
docker run -p 8888:8888 jupyter/scipy-notebook:2c80cf3537ca

Executing the command: jupyter notebook
[I 15:33:00.567 NotebookApp] Writing notebook server cookie secret to /home/jovyan/.local/share/jupyter/runtime/notebook_cookie_secret
[W 15:33:01.084 NotebookApp] WARNING: The notebook server is listening on all IP addresses and not using encryption. This is not recommended.
[I 15:33:01.150 NotebookApp] JupyterLab alpha preview extension loaded from /opt/conda/lib/python3.6/site-packages/jupyterlab
[I 15:33:01.150 NotebookApp] JupyterLab application directory is /opt/conda/share/jupyter/lab
[I 15:33:01.155 NotebookApp] Serving notebooks from local directory: /home/jovyan
[I 15:33:01.156 NotebookApp] 0 active kernels
[I 15:33:01.156 NotebookApp] The Jupyter Notebook is running at:
[I 15:33:01.157 NotebookApp] http://[all ip addresses on your system]:8888/?token=112bb073331f1460b73768c76dffb2f87ac1d4ca7870d46a
[I 15:33:01.157 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 15:33:01.160 NotebookApp]

    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://localhost:8888/?token=112bb073331f1460b73768c76dffb2f87ac1d4ca7870d46a
```

Pressing `Ctrl-C` shuts down the notebook server but leaves the container intact on disk for later restart or permanent deletion using commands like the following:

```
# list containers
docker ps -a
CONTAINER ID        IMAGE                   COMMAND                  CREATED    STATUS                      PORTS               NAMES
d67fe77f1a84        jupyter/base-notebook   "tini -- start-noteb…"   44 seconds ago    Exited (0) 39 seconds ago                       cocky_mirzakhani

# start the stopped container
docker start -a d67fe77f1a84
Executing the command: jupyter notebook
[W 16:45:02.020 NotebookApp] WARNING: The notebook server is listening on all IP addresses and not using encryption. This is not recommended.
...

# remove the stopped container
docker rm d67fe77f1a84
d67fe77f1a84
```

**Example 2** This command pulls the `jupyter/r-notebook` image tagged `e5c5a7d3e52d` from Docker Hub if it is not already present on the local host. It then starts a container running a Jupyter Notebook server and exposes the server on host port 10000. The server logs appear in the terminal and include a URL to the notebook server, but with the internal container port (8888) instead of the the correct host port (10000).

```
docker run --rm -p 10000:8888 -v "$PWD":/home/jovyan/work jupyter/r-notebook:e5c5a7d3e52d

Executing the command: jupyter notebook
[I 19:31:09.573 NotebookApp] Writing notebook server cookie secret to /home/jovyan/.local/share/jupyter/runtime/notebook_cookie_secret
[W 19:31:11.930 NotebookApp] WARNING: The notebook server is listening on all IP addresses and not using encryption. This is not recommended.
[I 19:31:12.085 NotebookApp] JupyterLab alpha preview extension loaded from /opt/conda/lib/python3.6/site-packages/jupyterlab
[I 19:31:12.086 NotebookApp] JupyterLab application directory is /opt/conda/share/jupyter/lab
[I 19:31:12.117 NotebookApp] Serving notebooks from local directory: /home/jovyan
[I 19:31:12.117 NotebookApp] 0 active kernels
[I 19:31:12.118 NotebookApp] The Jupyter Notebook is running at:
[I 19:31:12.119 NotebookApp] http://[all ip addresses on your system]:8888/?token=3b8dce890cb65570fb0d9c4a41ae067f7604873bd604f5ac
[I 19:31:12.120 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 19:31:12.122 NotebookApp]

    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://localhost:8888/?token=3b8dce890cb65570fb0d9c4a41ae067f7604873bd604f5ac
```

Pressing `Ctrl-C` shuts down the notebook server and immediately destroys the Docker container. Files written to `~/work` in the container remain touched. Any other changes made in the container are lost.

**Example 3** This command pulls the `jupyter/all-spark-notebook` image currently tagged `latest` from Docker Hub if an image tagged `latest` is not already present on the local host. It then starts a container named `notebook` running a JupyterLab server and exposes the server on a randomly selected port. 

```
docker run -d -P --name notebook jupyter/all-spark-notebook
```

The assigned port and notebook server token are visible using other Docker commands.

```
# get the random host port assigned to the container port 8888
docker port notebook 8888
0.0.0.0:32769

# get the notebook token from the logs
docker logs --tail 3 notebook
    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://localhost:8888/?token=15914ca95f495075c0aa7d0e060f1a78b6d94f70ea373b00
```

Together, the URL to visit on the host machine to access the server in this case is http://localhost:32769?token=15914ca95f495075c0aa7d0e060f1a78b6d94f70ea373b00.

The container runs in the background until stopped and/or removed by additional Docker commands.

```
# stop the container
docker stop notebook
notebook

# remove the container permanently
docker rm notebook
notebook
```

## Using Binder

[Binder](https://mybinder.org/) is a service that allows you to create and share custom computing environments for projects in version control. You can use any of the Jupyter Docker Stacks images as a basis for a Binder-compatible Dockerfile. See the [docker-stacks example](https://mybinder.readthedocs.io/en/latest/sample_repos.html#using-a-docker-image-from-the-jupyter-docker-stacks-repository) and [Using a Dockerfile](https://mybinder.readthedocs.io/en/latest/tutorials/dockerfile.html) sections in the [Binder documentation](https://mybinder.readthedocs.io/en/latest/index.html) for instructions.

## Using JupyterHub

You can configure JupyterHub to launcher Docker containers from the Jupyter Docker Stacks images. If you've been following the [Zero to JupyterHub with Kubernetes](http://zero-to-jupyterhub.readthedocs.io/en/latest/) guide, see the [Use an existing Docker image](http://zero-to-jupyterhub.readthedocs.io/en/latest/user-environment.html#use-an-existing-docker-image) section for details. If you have a custom JupyterHub deployment, see the [Picking or building a Docker image](https://github.com/jupyterhub/dockerspawner#picking-or-building-a-docker-image) instructions for the [dockerspawner](https://github.com/jupyterhub/dockerspawner) instead.

## Using Other Tools and Services

You can use the Jupyter Docker Stacks with any Docker-compatible technology (e.g., [Docker Compose](https://docs.docker.com/compose/), [docker-py](https://github.com/docker/docker-py), your favorite cloud container service). See the documentation of the tool, library, or service for details about how to reference, configure, and launch containers from these images.
