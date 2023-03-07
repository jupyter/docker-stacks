# Running a Container

Using one of the Jupyter Docker Stacks requires two choices:

1. Which Docker image you wish to use
2. How you wish to start Docker containers from that image

This section provides details about the second.

## Using the Docker CLI

You can launch a local Docker container from the Jupyter Docker Stacks using the [Docker command-line interface](https://docs.docker.com/engine/reference/commandline/cli/).
There are numerous ways to configure containers using the CLI.
The following are some common patterns.

**Example 1:**

This command pulls the `jupyter/scipy-notebook` image tagged `2023-02-28` from Docker Hub if it is not already present on the local host.
It then starts a container running a Jupyter Notebook server and exposes the server on host port 8888.
The server logs appear in the terminal and include a URL to the notebook server.

```bash
docker run -it -p 8888:8888 jupyter/scipy-notebook:2023-02-28

# Entered start.sh with args: jupyter lab

# ...

#     To access the server, open this file in a browser:
#         file:///home/jovyan/.local/share/jupyter/runtime/jpserver-7-open.html
#     Or copy and paste one of these URLs:
#         http://042fc8ac2b0c:8888/lab?token=f31f2625f13d131f578fced0fc76b81d10f6c629e92c7099
#      or http://127.0.0.1:8888/lab?token=f31f2625f13d131f578fced0fc76b81d10f6c629e92c7099
```

Pressing `Ctrl-C` twice shuts down the notebook server but leaves the container intact on disk for later restart or permanent deletion using commands like the following:

```bash
# list containers
docker ps -a
# CONTAINER ID   IMAGE                                                 COMMAND                  CREATED          STATUS                     PORTS     NAMES
# 221331c047c4   jupyter/scipy-notebook:2023-02-28                   "tini -g -- start-no…"   11 seconds ago   Exited (0) 8 seconds ago             cranky_benz

# start the stopped container
docker start -a 221331c047c4
# Entered start.sh with args: jupyter lab
# ...

# remove the stopped container
docker rm 221331c047c4
# 221331c047c4
```

**Example 2:**

This command pulls the `jupyter/r-notebook` image tagged `2023-02-28` from Docker Hub if it is not already present on the local host.
It then starts a container running a Jupyter Notebook server and exposes the server on host port 10000.
The server logs appear in the terminal and include a URL to the notebook server, but with the internal container port (8888) instead of the correct host port (10000).

```bash
docker run -it --rm -p 10000:8888 -v "${PWD}":/home/jovyan/work jupyter/r-notebook:2023-02-28
```

Pressing `Ctrl-C` twice shuts down the notebook server and immediately destroys the Docker container.
New files and changes in `~/work` in the container will be preserved.
Any other changes made in the container will be lost.

**Example 3:**

This command pulls the `jupyter/all-spark-notebook` image currently tagged `latest` from Docker Hub if an image tagged `latest` is not already present on the local host.
It then starts a container named `notebook` running a JupyterLab server and exposes the server on a randomly selected port.

```bash
docker run -d -P --name notebook jupyter/all-spark-notebook
```

where:

- `-d`: will run the container in detached mode

You can also use the following docker commands to see the port and notebook server token:

```bash
# get the random host port assigned to the container port 8888
docker port notebook 8888
# 0.0.0.0:49153
# :::49153

# get the notebook token from the logs
docker logs --tail 3 notebook
    # Or copy and paste one of these URLs:
    #     http://878f1a9b4dfa:8888/lab?token=d336fa63c03f064ff15ce7b269cab95b2095786cf9ab2ba3
    #  or http://127.0.0.1:8888/lab?token=d336fa63c03f064ff15ce7b269cab95b2095786cf9ab2ba3
```

Together, the URL to visit on the host machine to access the server, in this case, is <http://127.0.0.1:49153/lab?token=d336fa63c03f064ff15ce7b269cab95b2095786cf9ab2ba3>.

The container runs in the background until stopped and/or removed by additional Docker commands:

```bash
# stop the container
docker stop notebook
# notebook

# remove the container permanently
docker rm notebook
# notebook
```

## Using the Podman CLI

An alternative to using the Docker CLI is to use the Podman CLI. Podman is mostly compatible with Docker.

**Example 4:**

If we use Podman instead of Docker in the situation given in _Example 2_, it will look like this:

The example makes use of rootless Podman; in other words, the Podman command is run from a regular user account.
In a Bash shell, set the shell variables _uid_ and _gid_ to the UID and GID of the user _jovyan_ in the container.

```bash
uid=1000
gid=100
```

Set the shell variables _subuidSize_ and _subgidSize_ to the number of subordinate UIDs and GIDs, respectively.

```bash
subuidSize=$(( $(podman info --format "{{ range .Host.IDMappings.UIDMap }}+{{.Size }}{{end }}" ) - 1 ))
subgidSize=$(( $(podman info --format "{{ range .Host.IDMappings.GIDMap }}+{{.Size }}{{end }}" ) - 1 ))
```

This command pulls the `docker.io/jupyter/r-notebook` image tagged `2023-02-28` from Docker Hub if it is not already present on the local host.
It then starts a container running a Jupyter Server and exposes the server on host port 10000.
The server logs appear in the terminal and include a URL to the notebook server, but with the internal container port (8888) instead of the correct host port (10000).

```bash
podman run -it --rm -p 10000:8888 \
    -v "${PWD}":/home/jovyan/work --user $uid:$gid \
    --uidmap $uid:0:1 --uidmap 0:1:$uid --uidmap $(($uid+1)):$(($uid+1)):$(($subuidSize-$uid)) \
    --gidmap $gid:0:1 --gidmap 0:1:$gid --gidmap $(($gid+1)):$(($gid+1)):$(($subgidSize-$gid)) \
    docker.io/jupyter/r-notebook:2023-02-28
```

```{warning}
The `podman run` options `--uidmap` and `--gidmap` can be used to map the container user _jovyan_ to the regular user on the host when running rootless Podman.
The same Podman command should not be run with sudo (i.e. running rootful Podman)
because then the mapping would map the container user _jovyan_ to the root user on the host.
It's a good security practice to run programs with as few privileges as possible.
```

```{note}
The `podman run` command in the example above maps all subuids and subgids of the user into the container.
That works fine but is actually more than needed.
The `podman run` option `--userns=auto` will, for instance, not be possible to use as long as there are no unused subuids and subgids available.
The example could be improved by investigating more in detail which UIDs and GIDs need to be available in the container and then only map them.
```

Pressing `Ctrl-C` twice shuts down the notebook server and immediately destroys the Docker container.
New files and changes in `~/work` in the container will be preserved.
Any other changes made in the container will be lost.

## Using Binder

[Binder](https://mybinder.org/) is a service that allows you to create and share custom computing environments for projects in version control.
You can use any of the Jupyter Docker Stacks images as a basis for a Binder-compatible Dockerfile.
See the
[docker-stacks example](https://mybinder.readthedocs.io/en/latest/examples/sample_repos.html#using-a-docker-image-from-the-jupyter-docker-stacks-repository) and
[Using a Dockerfile](https://mybinder.readthedocs.io/en/latest/tutorials/dockerfile.html) sections in the
[Binder documentation](https://mybinder.readthedocs.io/en/latest/index.html) for instructions.

## Using JupyterHub

You can configure JupyterHub to launcher Docker containers from the Jupyter Docker Stacks images.
If you've been following the [Zero to JupyterHub with Kubernetes](https://z2jh.jupyter.org/en/latest/) guide,
see the [Use an existing Docker image](https://z2jh.jupyter.org/en/latest/jupyterhub/customizing/user-environment.html#choose-and-use-an-existing-docker-image) section for details.
If you have a custom JupyterHub deployment, see the [Picking or building a Docker image](https://jupyterhub-dockerspawner.readthedocs.io/en/latest/docker-image.html)
instructions for the [dockerspawner](https://github.com/jupyterhub/dockerspawner) instead.

## Using Other Tools and Services

You can use the Jupyter Docker Stacks with any Docker-compatible technology
(e.g., [Docker Compose](https://docs.docker.com/compose/), [docker-py](https://github.com/docker/docker-py), your favorite cloud container service).
See the documentation of the tool, library, or service for details about how to reference, configure, and launch containers from these images.
