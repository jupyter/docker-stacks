# Common Features

A container launched from any Jupyter Docker Stacks image runs a Jupyter Notebook server by default. The container does so by executing a `start-notebook.sh` script. This script configures the internal container environment and then runs `jupyter notebook`, passing it any command line arguments received.

This page describes the options supported by the startup script as well as how to bypass it to run alternative commands.

## Notebook Options

You can pass [Jupyter command line options](https://jupyter.readthedocs.io/en/latest/projects/jupyter-command.html) to the `start-notebook.sh` script when launching the container. For example, to secure the Notebook server with a custom password hashed using `IPython.lib.passwd()` instead of the default token, you can run the following:

```
docker run -d -p 8888:8888 jupyter/base-notebook start-notebook.sh --NotebookApp.password='sha1:74ba40f8a388:c913541b7ee99d15d5ed31d4226bf7838f83a50e'
```

For example, to set the base URL of the notebook server, you can run the following:

```
docker run -d -p 8888:8888 jupyter/base-notebook start-notebook.sh --NotebookApp.base_url=/some/path
```

## Docker Options

You may instruct the `start-notebook.sh` script to customize the container environment before launching
the notebook server. You do so by passing arguments to the `docker run` command.

* `-e NB_USER=jovyan` - Instructs the startup script to change the default container username from `jovyan` to the provided value. Causes the script to rename the `jovyan` user home folder. For this option to take effect, you must run the container with `--user root` and set the working directory `-w /home/$NB_USER`. This feature is useful when mounting host volumes with specific home folder.
* `-e NB_UID=1000` - Instructs the startup script to switch the numeric user ID of `$NB_USER` to the given value. This feature is useful when mounting host volumes with specific owner permissions. For this option to take effect, you must run the container with `--user root`. (The startup script will `su $NB_USER` after adjusting the user ID.) You might consider using modern Docker options `--user` and `--group-add` instead. See the last bullet below for details.
* `-e NB_GID=100` - Instructs the startup script to change the primary group of`$NB_USER` to `$NB_GID` (the new group is added with a name of `$NB_GROUP` if it is defined, otherwise the group is named `$NB_USER`).  This feature is useful when mounting host volumes with specific group permissions. For this option to take effect, you must run the container with `--user root`. (The startup script will `su $NB_USER` after adjusting the group ID.) You might consider using modern Docker options `--user` and `--group-add` instead. See the last bullet below for details.  The user is added to supplemental group `users` (gid 100) in order to allow write access to the home directory and `/opt/conda`.  If you override the user/group logic, ensure the user stays in group `users` if you want them to be able to modify files in the image.
* `-e NB_GROUP=<name>` - The name used for `$NB_GID`, which defaults to `$NB_USER`.  This is only used if `$NB_GID` is specified and completely optional: there is only cosmetic effect.
* `-e NB_UMASK=<umask>` - Configures Jupyter to use a different umask value from default, i.e. `022`. For example, if setting umask to `002`, new files will be readable and writable by group members instead of just writable by the owner. Wikipedia has a good article about [umask](https://en.wikipedia.org/wiki/Umask). Feel free to read it in order to choose the value that better fits your needs. Default value should fit most situations. Note that `NB_UMASK` when set only applies to the Jupyter process itself - you cannot use it to set a umask for additional files created during run-hooks e.g. via `pip` or `conda` - if you need to set a umask for these you must set `umask` for each command.
* `-e CHOWN_HOME=yes` - Instructs the startup script to change the `$NB_USER` home directory owner and group to the current value of `$NB_UID` and `$NB_GID`. This change will take effect even if the user home directory is mounted from the host using `-v` as described below. The change is **not** applied recursively by default. You can change modify the `chown` behavior by setting `CHOWN_HOME_OPTS` (e.g., `-e CHOWN_HOME_OPTS='-R'`).
* `-e CHOWN_EXTRA="<some dir>,<some other dir>"` - Instructs the startup script to change the owner and group of each comma-separated container directory to the current value of `$NB_UID` and `$NB_GID`. The change is **not** applied recursively by default. You can change modify the `chown` behavior by setting `CHOWN_EXTRA_OPTS` (e.g., `-e CHOWN_EXTRA_OPTS='-R'`).
* `-e GRANT_SUDO=yes` - Instructs the startup script to grant the `NB_USER` user passwordless `sudo` capability. You do **not** need this option to allow the user to `conda` or `pip` install additional packages. This option is useful, however, when you wish to give `$NB_USER` the ability to install OS packages with `apt` or modify other root-owned files in the container. For this option to take effect, you must run the container with `--user root`. (The `start-notebook.sh` script will `su $NB_USER` after adding `$NB_USER` to sudoers.) **You should only enable `sudo` if you trust the user or if the container is running on an isolated host.**
* `-e GEN_CERT=yes` - Instructs the startup script to generates a self-signed SSL certificate and configure Jupyter Notebook to use it to accept encrypted HTTPS connections.
* `-e JUPYTER_ENABLE_LAB=yes` - Instructs the startup script to run `jupyter lab` instead of the default `jupyter notebook` command. Useful in container orchestration environments where setting environment variables is easier than change command line parameters.
* `-v /some/host/folder/for/work:/home/jovyan/work` - Mounts a host machine directory as folder in the container. Useful when you want to preserve notebooks and other work even after the container is destroyed. **You must grant the within-container notebook user or group (`NB_UID` or `NB_GID`) write access to the host directory (e.g., `sudo chown 1000 /some/host/folder/for/work`).**
* `--user 5000 --group-add users` - Launches the container with a specific user ID and adds that user to the `users` group so that it can modify files in the default home directory and `/opt/conda`. You can use these arguments as alternatives to setting `$NB_UID` and `$NB_GID`.

## Startup Hooks

You can further customize the container environment by adding shell scripts (`*.sh`) to be sourced
or executables (`chmod +x`) to be run to the paths below:

* `/usr/local/bin/start-notebook.d/` - handled before any of the standard options noted above
  are applied
* `/usr/local/bin/before-notebook.d/` - handled after all of the standard options noted above are
  applied and just before the notebook server launches

See the `run-hooks` function in the [`jupyter/base-notebook start.sh`](https://github.com/jupyter/docker-stacks/blob/master/base-notebook/start.sh)
script for execution details.

## SSL Certificates

You may mount SSL key and certificate files into a container and configure Jupyter Notebook to use them to accept HTTPS connections. For example, to mount a host folder containing a `notebook.key` and `notebook.crt` and use them, you might run the following:

```
docker run -d -p 8888:8888 \
    -v /some/host/folder:/etc/ssl/notebook \
    jupyter/base-notebook start-notebook.sh \
    --NotebookApp.keyfile=/etc/ssl/notebook/notebook.key
    --NotebookApp.certfile=/etc/ssl/notebook/notebook.crt
```

Alternatively, you may mount a single PEM file containing both the key and certificate. For example:

```
docker run -d -p 8888:8888 \
    -v /some/host/folder/notebook.pem:/etc/ssl/notebook.pem \
    jupyter/base-notebook start-notebook.sh \
    --NotebookApp.certfile=/etc/ssl/notebook.pem
```

In either case, Jupyter Notebook expects the key and certificate to be a base64 encoded text file. The certificate file or PEM may contain one or more certificates (e.g., server, intermediate, and root).

For additional information about using SSL, see the following:

* The [docker-stacks/examples](https://github.com/jupyter/docker-stacks/tree/master/examples) for information about how to use [Let's Encrypt](https://letsencrypt.org/) certificates when you run these stacks on a publicly visible domain.
* The [jupyter_notebook_config.py](jupyter_notebook_config.py) file for how this Docker image generates a self-signed certificate.
* The [Jupyter Notebook documentation](https://jupyter-notebook.readthedocs.io/en/latest/public_server.html#securing-a-notebook-server) for best practices about securing a public notebook server in general.

## Alternative Commands

### start.sh

The `start-notebook.sh` script actually inherits most of its option handling capability from a more generic `start.sh` script. The `start.sh` script supports all of the features described above, but allows you to specify an arbitrary command to execute. For example, to run the text-based `ipython` console in a container, do the following:

```
docker run -it --rm jupyter/base-notebook start.sh ipython
```

Or, to run JupyterLab instead of the classic notebook, run the following:

```
docker run -it --rm -p 8888:8888 jupyter/base-notebook start.sh jupyter lab
```

This script is particularly useful when you derive a new Dockerfile from this image and install additional Jupyter applications with subcommands like `jupyter console`, `jupyter kernelgateway`, etc.

### Others

You can bypass the provided scripts and specify your an arbitrary start command. If you do, keep in mind that features supported by the `start.sh` script and its kin will not function (e.g., `GRANT_SUDO`).

## Conda Environments

The default Python 3.x [Conda environment](http://conda.pydata.org/docs/using/envs.html) resides in `/opt/conda`. The `/opt/conda/bin` directory is part of the default `jovyan` user's `$PATH`. That directory is also whitelisted for use in `sudo` commands by the `start.sh` script.

The `jovyan` user has full read/write access to the `/opt/conda` directory. You can use either `conda` or `pip` to install new packages without any additional permissions.

```
# install a package into the default (python 3.x) environment
pip install some-package
conda install some-package
```

