![docker pulls](https://img.shields.io/docker/pulls/jupyter/tensorflow-notebook.svg) ![docker stars](https://img.shields.io/docker/stars/jupyter/tensorflow-notebook.svg) [![](https://images.microbadger.com/badges/image/jupyter/tensorflow-notebook.svg)](https://microbadger.com/images/jupyter/tensorflow-notebook "jupyter/tensorflow-notebook image metadata")

# Jupyter Notebook Scientific Python Stack + Tensorflow

## What it Gives You

* Everything in [Scipy Notebook](https://github.com/jupyter/docker-stacks/tree/master/scipy-notebook)
* Tensorflow for Python 2.7 and 3.5 (without GPU support)

## Basic Use

The following command starts a container with the Notebook server listening for HTTP connections on port 8888 with a randomly generated authentication token configured.

```
docker run -it --rm -p 8888:8888 jupyter/tensorflow-notebook
```

Take note of the authentication token included in the notebook startup log messages. Include it in the URL you visit to access the Notebook server or enter it in the Notebook login form.

## Tensorflow Single Machine Mode

As distributed tensorflow is still immature, we currently only provide the single machine mode.

```
import tensorflow as tf

hello = tf.Variable('Hello World!')

sess = tf.Session()
init = tf.global_variables_initializer()

sess.run(init)
sess.run(hello)
```

## Notebook Options

The Docker container executes a [`start-notebook.sh` script](../base-notebook/start-notebook.sh) script by default. The `start-notebook.sh` script handles the `NB_UID`, `NB_GID` and `GRANT_SUDO` features documented in the next section, and then executes the `jupyter notebook`.

You can pass [Jupyter command line options](https://jupyter.readthedocs.io/en/latest/projects/jupyter-command.html) through the `start-notebook.sh` script when launching the container. For example, to secure the Notebook server with a custom password hashed using `IPython.lib.passwd()` instead of the default token, run the following:

```
docker run -d -p 8888:8888 jupyter/tensorflow-notebook start-notebook.sh --NotebookApp.password='sha1:74ba40f8a388:c913541b7ee99d15d5ed31d4226bf7838f83a50e'
```

For example, to set the base URL of the notebook server, run the following:

```
docker run -d -p 8888:8888 jupyter/tensorflow-notebook start-notebook.sh --NotebookApp.base_url=/some/path
```

For example, to disable all authentication mechanisms (not a recommended practice):

```
docker run -d -p 8888:8888 jupyter/tensorflow-notebook start-notebook.sh --NotebookApp.token=''
```

You can sidestep the `start-notebook.sh` script and run your own commands in the container. See the *Alternative Commands* section later in this document for more information.

## Docker Options

You may customize the execution of the Docker container and the command it is running with the following optional arguments.

* `-e GEN_CERT=yes` - Generates a self-signed SSL certificate and configures Jupyter Notebook to use it to accept encrypted HTTPS connections.
* `-e NB_UID=1000` - Specify the uid of the `jovyan` user. Useful to mount host volumes with specific file ownership. For this option to take effect, you must run the container with `--user root`. (The `start-notebook.sh` script will `su jovyan` after adjusting the user id.)
* `-e NB_GID=100` - Specify the gid of the `jovyan` user. Useful to mount host volumes with specific file ownership. For this option to take effect, you must run the container with `--user root`. (The `start-notebook.sh` script will `su jovyan` after adjusting the group id.)
* `-e GRANT_SUDO=yes` - Gives the `jovyan` user passwordless `sudo` capability. Useful for installing OS packages. For this option to take effect, you must run the container with `--user root`. (The `start-notebook.sh` script will `su jovyan` after adding `jovyan` to sudoers.) **You should only enable `sudo` if you trust the user or if the container is running on an isolated host.**
* `-v /some/host/folder/for/work:/home/jovyan/work` - Host mounts the default working directory on the host to preserve work even when the container is destroyed and recreated (e.g., during an upgrade).

## SSL Certificates

You may mount SSL key and certificate files into a container and configure Jupyter Notebook to use them to accept HTTPS connections. For example, to mount a host folder containing a `notebook.key` and `notebook.crt`:

```
docker run -d -p 8888:8888 \
    -v /some/host/folder:/etc/ssl/notebook \
    jupyter/tensorflow-notebook start-notebook.sh \
    --NotebookApp.keyfile=/etc/ssl/notebook/notebook.key
    --NotebookApp.certfile=/etc/ssl/notebook/notebook.crt
```

Alternatively, you may mount a single PEM file containing both the key and certificate. For example:

```
docker run -d -p 8888:8888 \
    -v /some/host/folder/notebook.pem:/etc/ssl/notebook.pem \
    jupyter/tensorflow-notebook start-notebook.sh \
    --NotebookApp.certfile=/etc/ssl/notebook.pem
```

In either case, Jupyter Notebook expects the key and certificate to be a base64 encoded text file. The certificate file or PEM may contain one or more certificates (e.g., server, intermediate, and root).

For additional information about using SSL, see the following:

* The [docker-stacks/examples](https://github.com/jupyter/docker-stacks/tree/master/examples) for information about how to use [Let's Encrypt](https://letsencrypt.org/) certificates when you run these stacks on a publicly visible domain.
* The [jupyter_notebook_config.py](jupyter_notebook_config.py) file for how this Docker image generates a self-signed certificate.
* The [Jupyter Notebook documentation](https://jupyter-notebook.readthedocs.io/en/latest/public_server.html#using-ssl-for-encrypted-communication) for best practices about running a public notebook server in general, most of which are encoded in this image.


## Conda Environments

The default Python 3.x [Conda environment](http://conda.pydata.org/docs/using/envs.html) resides in `/opt/conda`. 

The commands `jupyter`, `ipython`, `python`, `pip`, and `conda` (among others) are available in both environments. For convenience, you can install packages into either environment regardless of what environment is currently active using commands like the following:

```
# install a package into the default (python 3.x) environment
pip install some-package
conda install some-package
```


## Alternative Commands

### start-singleuser.sh

[JupyterHub](https://jupyterhub.readthedocs.io) requires a single-user instance of the Jupyter Notebook server per user.   To use this stack with JupyterHub and [DockerSpawner](https://github.com/jupyter/dockerspawner), you must specify the container image name and override the default container run command in your `jupyterhub_config.py`:

```python
# Spawn user containers from this image
c.DockerSpawner.container_image = 'jupyter/tensorflow-notebook'

# Have the Spawner override the Docker run command
c.DockerSpawner.extra_create_kwargs.update({
	'command': '/usr/local/bin/start-singleuser.sh'
})
```

### start.sh

The `start.sh` script supports the same features as the default `start-notebook.sh` script (e.g., `GRANT_SUDO`), but allows you to specify an arbitrary command to execute. For example, to run the text-based `ipython` console in a container, do the following:

```
docker run -it --rm jupyter/tensorflow-notebook start.sh ipython
```

This script is particularly useful when you derive a new Dockerfile from this image and install additional Jupyter applications with subcommands like `jupyter console`, `jupyter kernelgateway`, and `jupyter lab`.

### Others

You can bypass the provided scripts and specify your an arbitrary start command. If you do, keep in mind that certain features documented above will not function (e.g., `GRANT_SUDO`).
