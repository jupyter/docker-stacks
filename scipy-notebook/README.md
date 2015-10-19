# Jupyter Notebook Scientific Python Stack

## What it Gives You

* Jupyter Notebook 4.0.x
* Conda Python 3.x and Python 2.7.x environments
* pandas, matplotlib, scipy, seaborn, scikit-learn, scikit-image, sympy, cython, patsy, statsmodel, cloudpickle, dill, numba, bokeh pre-installed
* Unprivileged user `jovyan` (uid=1000, configurable, see options) in group `users` (gid=100) with ownership over `/home/jovyan` and `/opt/conda`
* [tini](https://github.com/krallin/tini) as the container entrypoint and [start-notebook.sh](../minimal-notebook/start-notebook.sh) as the default command
* Options for HTTPS, password auth, and passwordless `sudo`

## Basic Use

The following command starts a container with the Notebook server listening for HTTP connections on port 8888 without authentication configured.

```
docker run -d -p 8888:8888 jupyter/scipy-notebook
```

## Notebook Options

You can pass [Jupyter command line options](http://jupyter.readthedocs.org/en/latest/config.html#command-line-arguments) through the [`start-notebook.sh` command](https://github.com/jupyter/docker-stacks/blob/master/minimal-notebook/start-notebook.sh#L15) when launching the container. For example, to set the base URL of the notebook server you might do the following:

```
docker run -d -p 8888:8888 jupyter/scipy-notebook start-notebook.sh --NotebookApp.base_url=/some/path
```

You can use this same approach to sidestep the `start-notebook.sh` script and run another command entirely. But be aware that this script does the final `su` to the `jovyan` user before running the notebook server, after doing what is necessary for the `NB_USER` and `GRANT_SUDO` features documented below.

## Docker Options

You may customize the execution of the Docker container and the Notebook server it contains with the following optional arguments.

* `-e PASSWORD="YOURPASS"` - Configures Jupyter Notebook to require the given password. Should be conbined with `USE_HTTPS` on untrusted networks.
* `-e USE_HTTPS=yes` - Configures Jupyter Notebook to accept encrypted HTTPS connections. If a `pem` file containing a SSL certificate and key is not found in `/home/jovyan/.ipython/profile_default/security/notebook.pem`, the container will generate a self-signed certificate for you.
* `-e NB_UID=1000` - Specify the uid of the `jovyan` user. Useful to mount host volumes with specific file ownership.
* `-e GRANT_SUDO=yes` - Gives the `jovyan` user passwordless `sudo` capability. Useful for installing OS packages. **You should only enable `sudo` if you trust the user or if the container is running on an isolated host.**
* `-v /some/host/folder/for/work:/home/jovyan/work` - Host mounts the default working directory on the host to preserve work even when the container is destroyed and recreated (e.g., during an upgrade).
* `-v /some/host/folder/for/server.pem:/home/jovyan/.local/share/jupyter/notebook.pem` - Mounts a SSL certificate plus key for `USE_HTTPS`. Useful if you have a real certificate for the domain under which you are running the Notebook server.

## Conda Environments

The default Python 3.x [Conda environment](http://conda.pydata.org/docs/using/envs.html) resides in `/opt/conda`. A second Python 2.x Conda environment exists in `/opt/conda/envs/python2`. You can [switch to the python2 environment](http://conda.pydata.org/docs/using/envs.html#change-environments-activate-deactivate) in a shell by entering the following:

```
source activate python2
```

You can return to the default environment with this command:

```
source deactivate
```

The commands `ipython`, `python`, `pip`, `easy_install`, and `conda` (among others) are available in both environments.
