![docker pulls](https://img.shields.io/docker/pulls/jupyter/base-notebook.svg) ![docker stars](https://img.shields.io/docker/stars/jupyter/base-notebook.svg) [![](https://images.microbadger.com/badges/image/jupyter/base-notebook.svg)](https://microbadger.com/images/jupyter/base-notebook "jupyter/base-notebook image metadata")

# Base Jupyter Notebook Stack

Small base image for defining your own stack

## What it Gives You

* Minimally-functional Jupyter Notebook 4.2.x (e.g., no pandoc for document conversion)
* Miniconda Python 3.x
* No preinstalled scientific computing packages
* Unprivileged user `jovyan` (uid=1000, configurable, see options) in group `users` (gid=100) with ownership over `/home/jovyan` and `/opt/conda`
* [tini](https://github.com/krallin/tini) as the container entrypoint and [start-notebook.sh](./start-notebook.sh) as the default command
* A [start-singleuser.sh](./start-singleuser.sh) script useful for running a single-user instance of the Notebook server, as required by JupyterHub
* A [start.sh](./start.sh) script useful for running alternative commands in the container (e.g. `ipython`, `jupyter kernelgateway`, `jupyter lab`)
* Options for HTTPS, password auth, and passwordless `sudo`

## Basic Use

The following command starts a container with the Notebook server listening for HTTP connections on port 8888 without authentication configured.

```
docker run -d -p 8888:8888 jupyter/base-notebook
```

## Notebook Options

The Docker container executes a [`start-notebook.sh` script](./start-notebook.sh) script by default. The `start-notebook.sh` script handles the `NB_UID` and `GRANT_SUDO` features documented in the next section, and then executes the `jupyter notebook`.

You can pass [Jupyter command line options](https://jupyter.readthedocs.io/en/latest/projects/jupyter-command.html) through the `start-notebook.sh` script when launching the container. For example, to secure the Notebook server with a password hashed using `IPython.lib.passwd()`, run the following:

```
docker run -d -p 8888:8888 jupyter/base-notebook start-notebook.sh --NotebookApp.password='sha1:74ba40f8a388:c913541b7ee99d15d5ed31d4226bf7838f83a50e'
```

For example, to set the base URL of the notebook server, run the following:

```
docker run -d -p 8888:8888 jupyter/base-notebook start-notebook.sh --NotebookApp.base_url=/some/path
```

You can sidestep the `start-notebook.sh` script and run your own commands in the container. See the *Alternative Commands* section later in this document for more information.

## Docker Options

You may customize the execution of the Docker container and the command it is running with the following optional arguments.

* `-e PASSWORD="YOURPASS"` - Configures Jupyter Notebook to require the given plain-text password. Should be combined with `USE_HTTPS` on untrusted networks. **Note** that this option is not as secure as passing a pre-hashed password on the command line as shown above.
* `-e USE_HTTPS=yes` - Configures Jupyter Notebook to accept encrypted HTTPS connections. If a `pem` file containing a SSL certificate and key is not provided (see below), the container will generate a self-signed certificate for you.
* `-e NB_UID=1000` - Specify the uid of the `jovyan` user. Useful to mount host volumes with specific file ownership. For this option to take effect, you must run the container with `--user root`. (The `start-notebook.sh` script will `su jovyan` after adjusting the user id.)
* `-e GRANT_SUDO=yes` - Gives the `jovyan` user passwordless `sudo` capability. Useful for installing OS packages. For this option to take effect, you must run the container with `--user root`. (The `start-notebook.sh` script will `su jovyan` after adding `jovyan` to sudoers.) **You should only enable `sudo` if you trust the user or if the container is running on an isolated host.**
* `-v /some/host/folder/for/work:/home/jovyan/work` - Host mounts the default working directory on the host to preserve work even when the container is destroyed and recreated (e.g., during an upgrade).
* `-v /some/host/folder/for/server.pem:/home/jovyan/.local/share/jupyter/notebook.pem` - Mounts a SSL certificate plus key for `USE_HTTPS`. Useful if you have a real certificate for the domain under which you are running the Notebook server.

## SSL Certificates

The notebook server configuration in this Docker image expects the `notebook.pem` file mentioned above to contain a base64 encoded SSL key and at least one base64 encoded SSL certificate. The file may contain additional certificates (e.g., intermediate and root certificates).

If you have your key and certificate(s) as separate files, you must concatenate them together into the single expected PEM file. Alternatively, you can build your own configuration and Docker image in which you pass the key and certificate separately.

For additional information about using SSL, see the following:

* The [docker-stacks/examples](https://github.com/jupyter/docker-stacks/tree/master/examples) for information about how to use [Let's Encrypt](https://letsencrypt.org/) certificates when you run these stacks on a publicly visible domain.
* The [jupyter_notebook_config.py](jupyter_notebook_config.py) file for how this Docker image generates a self-signed certificate.
* The [Jupyter Notebook documentation](https://jupyter-notebook.readthedocs.io/en/latest/public_server.html#using-ssl-for-encrypted-communication) for best practices about running a public notebook server in general, most of which are encoded in this image.

## Conda Environment

The default Python 3.x [Conda environment](http://conda.pydata.org/docs/using/envs.html) resides in `/opt/conda`. The commands `ipython`, `python`, `pip`, `easy_install`, and `conda` (among others) are available in this environment.

## Alternative Commands

### start-singleuser.sh

[JupyterHub](https://jupyterhub.readthedocs.io) requires a single-user instance of the Jupyter Notebook server per user.   To use this stack with JupyterHub and [DockerSpawner](https://github.com/jupyter/dockerspawner), you must specify the container image name and override the default container run command in your `jupyterhub_config.py`:

```python
# Spawn user containers from this image
c.DockerSpawner.container_image = 'jupyter/base-notebook'

# Have the Spawner override the Docker run command
c.DockerSpawner.extra_create_kwargs.update({
	'command': '/usr/local/bin/start-singleuser.sh'
})
```

### start.sh

The `start.sh` script supports the same features as the default `start-notebook.sh` script (e.g., `GRANT_SUDO`), but allows you to specify an arbitrary command to execute. For example, to run the text-based `ipython` console in a container, do the following:

```
docker run -it --rm jupyter/base-notebook start.sh ipython
```

This script is particularly useful when you derive a new Dockerfile from this image and install additional Jupyter applications with subcommands like `jupyter console`, `jupyter kernelgateway`, and `jupyter lab`.

### Others

You can bypass the provided scripts and specify your an arbitrary start command. If you do, keep in mind that certain features documented above will not function (e.g., `GRANT_SUDO`).
