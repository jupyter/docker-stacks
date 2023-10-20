# Common Features

Except for `jupyter/docker-stacks-foundation`, a container launched from any Jupyter Docker Stacks image runs a Jupyter Server with the JupyterLab frontend.
The container does so by executing a `start-notebook.py` script.
This script configures the internal container environment and then runs `jupyter lab`, passing any command-line arguments received.

This page describes the options supported by the startup script and how to bypass it to run alternative commands.

## Jupyter Server Options

You can pass [Jupyter Server options](https://jupyter-server.readthedocs.io/en/latest/operators/public-server.html) to the `start-notebook.py` script when launching the container.

1. For example, to secure the Jupyter Server with a [custom password](https://jupyter-server.readthedocs.io/en/latest/operators/public-server.html#preparing-a-hashed-password)
   hashed using `jupyter_server.auth.passwd()` instead of the default token,
   you can run the following (this hash was generated for the `my-password` password):

   ```bash
   docker run -it --rm -p 8888:8888 quay.io/jupyter/base-notebook \
       start-notebook.py --PasswordIdentityProvider.hashed_password='argon2:$argon2id$v=19$m=10240,t=10,p=8$JdAN3fe9J45NvK/EPuGCvA$O/tbxglbwRpOFuBNTYrymAEH6370Q2z+eS1eF4GM6Do'
   ```

2. To set the [base URL](https://jupyter-server.readthedocs.io/en/latest/operators/public-server.html#running-the-notebook-with-a-customized-url-prefix) of the Jupyter Server, you can run the following:

   ```bash
   docker run  -it --rm -p 8888:8888 quay.io/jupyter/base-notebook \
       start-notebook.py --ServerApp.base_url=/customized/url/prefix/
   ```

## Docker Options

You may instruct the `start-notebook.py` script to customize the container environment before launching the Server.
You do so by passing arguments to the `docker run` command.

### User-related configurations

- `-e NB_USER=<username>` - The desired username and associated home folder.
  The default value is `jovyan`.
  Setting `NB_USER` refits the `jovyan` default user and ensures that the desired user has the correct file permissions
  for the new home directory created at `/home/<username>`.
  For this option to take effect, you **must** run the container with `--user root`, set the working directory `-w "/home/<username>"`
  and set the environment variable `-e CHOWN_HOME=yes`.

  _Example usage:_

  ```bash
  docker run -it --rm \
      -p 8888:8888 \
      --user root \
      -e NB_USER="my-username" \
      -e CHOWN_HOME=yes \
      -w "/home/my-username" \
      quay.io/jupyter/base-notebook
  ```

- `-e NB_UID=<numeric uid>` - Instructs the startup script to switch the numeric user ID of `${NB_USER}` to the given value.
  The default value is `1000`.
  This feature is useful when mounting host volumes with specific owner permissions.
  You **must** run the container with `--user root` for this option to take effect.
  (The startup script will `su ${NB_USER}` after adjusting the user ID.)
  Instead, you might consider using the modern Docker-native options [`--user`](https://docs.docker.com/engine/reference/run/#user) and
  [`--group-add`](https://docs.docker.com/engine/reference/run/#additional-groups) - see the last bullet in this section for more details.
  See bullet points regarding `--user` and `--group-add`.

- `-e NB_GID=<numeric gid>` - Instructs the startup script to change the primary group of `${NB_USER}` to `${NB_GID}`
  (the new group is added with a name of `${NB_GROUP}` if it is defined. Otherwise, the group is named `${NB_USER}`).
  This feature is useful when mounting host volumes with specific group permissions.
  You **must** run the container with `--user root` for this option to take effect.
  (The startup script will `su ${NB_USER}` after adjusting the group ID.)
  Instead, you might consider using modern Docker options `--user` and `--group-add`.
  See bullet points regarding `--user` and `--group-add`.
  The user is added to the supplemental group `users` (gid 100) to grant write access to the home directory and `/opt/conda`.
  If you override the user/group logic, ensure the user stays in the group `users` if you want them to be able to modify files in the image.

- `-e NB_GROUP=<name>` - The name used for `${NB_GID}`, which defaults to `${NB_USER}`.
  This group name is only used if `${NB_GID}` is specified and completely optional: there is only a cosmetic effect.

- `--user 5000 --group-add users` - Launches the container with a specific user ID and adds that user to the `users` group so that it can modify files in the default home directory and `/opt/conda`.
  You can use these arguments as alternatives to setting `${NB_UID}` and `${NB_GID}`.

## Permission-specific configurations

- `-e NB_UMASK=<umask>` - Configures Jupyter to use a different `umask` value from default, i.e. `022`.
  For example, if setting `umask` to `002`, new files will be readable and writable by group members instead of the owner only.
  [Check this Wikipedia article](https://en.wikipedia.org/wiki/Umask) for an in-depth description of `umask` and suitable values for multiple needs.
  While the default `umask` value should be sufficient for most use cases, you can set the `NB_UMASK` value to fit your requirements.

  ```{note}
  `NB_UMASK` when set only applies to the Jupyter process itself -
  you cannot use it to set a `umask` for additional files created during `run-hooks.sh`.
  For example, via `pip` or `conda`.
  If you need to set a `umask` for these, you **must** set the `umask` value for each command.
  ```

- `-e CHOWN_HOME=yes` - Instructs the startup script to change the `${NB_USER}` home directory owner and group to the current value of `${NB_UID}` and `${NB_GID}`.
  This change will take effect even if the user home directory is mounted from the host using `-v` as described below.
  The change is **not** applied recursively by default.
  You can modify the `chown` behavior by setting `CHOWN_HOME_OPTS` (e.g., `-e CHOWN_HOME_OPTS='-R'`).

- `-e CHOWN_EXTRA="<some dir>,<some other dir>"` - Instructs the startup script to change the owner and group of each comma-separated container directory to the current value of `${NB_UID}` and `${NB_GID}`.
  The change is **not** applied recursively by default.
  You can modify the `chown` behavior by setting `CHOWN_EXTRA_OPTS` (e.g., `-e CHOWN_EXTRA_OPTS='-R'`).

- `-e GRANT_SUDO=yes` - Instructs the startup script to grant the `NB_USER` user passwordless `sudo` capability.
  You do **not** need this option to allow the user to `conda` or `pip` install additional packages.
  This option is helpful for cases when you wish to give `${NB_USER}` the ability to install OS packages with `apt` or modify other root-owned files in the container.
  You **must** run the container with `--user root` for this option to take effect.
  (The `start-notebook.py` script will `su ${NB_USER}` after adding `${NB_USER}` to sudoers.)
  **You should only enable `sudo` if you trust the user or if the container runs on an isolated host.**

### Additional runtime configurations

- `-e GEN_CERT=yes` - Instructs the startup script to generate a self-signed SSL certificate.
  Configures Jupyter Server to use it to accept encrypted HTTPS connections.
- `-e DOCKER_STACKS_JUPYTER_CMD=<jupyter command>` - Instructs the startup script to run `jupyter ${DOCKER_STACKS_JUPYTER_CMD}` instead of the default `jupyter lab` command.
  See [Switching back to the classic notebook or using a different startup command][switch_back] for available options.
  This setting is helpful in container orchestration environments where setting environment variables is more straightforward than changing command line parameters.
- `-e RESTARTABLE=yes` - Runs Jupyter in a loop so that quitting Jupyter does not cause the container to exit.
  This may be useful when installing extensions that require restarting Jupyter.
- `-v /some/host/folder/for/work:/home/jovyan/work` - Mounts a host machine directory as a folder in the container.
  This configuration is useful for preserving notebooks and other work even after the container is destroyed.
  **You must grant the within-container notebook user or group (`NB_UID` or `NB_GID`) write access to the host directory (e.g., `sudo chown 1000 /some/host/folder/for/work`).**
- `-e JUPYTER_ENV_VARS_TO_UNSET=ADMIN_SECRET_1,ADMIN_SECRET_2` - Unsets specified environment variables in the default startup script.
  The variables are unset after the hooks have been executed but before the command provided to the startup script runs.
- `-e NOTEBOOK_ARGS="--log-level='DEBUG' --dev-mode"` - Adds custom options to add to `jupyter` commands.
  This way, the user could use any option supported by the `jupyter` subcommand.
- `-e JUPYTER_PORT=8117` - Changes the port in the container that Jupyter is using to the value of the `${JUPYTER_PORT}` environment variable.
  This may be useful if you run multiple instances of Jupyter in swarm mode and want to use a different port for each instance.

## Startup Hooks

You can further customize the container environment by adding shell scripts (`*.sh`) to be sourced
or executables (`chmod +x`) to be run to the paths below:

- `/usr/local/bin/start-notebook.d/` - handled **before** any of the standard options noted above are applied
- `/usr/local/bin/before-notebook.d/` - handled **after** all the standard options noted above are applied
  and ran right before the Server launches

See the `run-hooks.sh` script [here](https://github.com/jupyter/docker-stacks/blob/main/images/docker-stacks-foundation/run-hooks.sh) and how it's used in the [`start.sh`](https://github.com/jupyter/docker-stacks/blob/main/images/docker-stacks-foundation/start.sh)
script for execution details.

## SSL Certificates

You may mount an SSL key and certificate file into a container and configure the Jupyter Server to use them to accept HTTPS connections.
For example, to mount a host folder containing a `notebook.key` and `notebook.crt` and use them, you might run the following:

```bash
docker run -it --rm -p 8888:8888 \
    -v /some/host/folder:/etc/ssl/notebook \
    quay.io/jupyter/base-notebook \
    start-notebook.py \
    --ServerApp.keyfile=/etc/ssl/notebook/notebook.key \
    --ServerApp.certfile=/etc/ssl/notebook/notebook.crt
```

Alternatively, you may mount a single PEM file containing both the key and certificate.
For example:

```bash
docker run -it --rm -p 8888:8888 \
    -v /some/host/folder/notebook.pem:/etc/ssl/notebook.pem \
    quay.io/jupyter/base-notebook \
    start-notebook.py \
    --ServerApp.certfile=/etc/ssl/notebook.pem
```

In either case, Jupyter Server expects the key and certificate to be a **base64 encoded text file**.
The certificate file or PEM may contain one or more certificates (e.g., server, intermediate, and root).

For additional information about using SSL, see the following:

- The [docker-stacks/examples](https://github.com/jupyter/docker-stacks/tree/main/examples)
  for information about how to use
  [Let's Encrypt](https://letsencrypt.org/) certificates when you run these stacks on a publicly visible domain.
- The [`jupyter_server_config.py`](https://github.com/jupyter/docker-stacks/blob/main/images/base-notebook/jupyter_server_config.py)
  file for how this Docker image generates a self-signed certificate.
- The [Jupyter Server documentation](https://jupyter-server.readthedocs.io/en/latest/operators/public-server.html#securing-a-jupyter-server)
  for best practices about securing a public Server in general.

## Alternative Commands

### Switching back to the classic notebook or using a different startup command

JupyterLab, built on top of Jupyter Server, is now the default for all the images of the stack.
However, switching back to the classic notebook or using a different startup command is still possible.
You can achieve this by setting the environment variable `DOCKER_STACKS_JUPYTER_CMD` at container startup.
The table below shows some options.
Since `Jupyter Notebook v7` `jupyter-server` is used as a backend.

| `DOCKER_STACKS_JUPYTER_CMD` | Frontend         |
| --------------------------- | ---------------- |
| `lab` (default)             | JupyterLab       |
| `notebook`                  | Jupyter Notebook |
| `nbclassic`                 | NbClassic        |
| `server`                    | None             |
| `retro`\*                   | RetroLab         |

```{note}
- Changing frontend for **JupyterHub singleuser image** is described in [JupyterHub docs](https://jupyterhub.readthedocs.io/en/latest/howto/configuration/config-user-env.html#switching-back-to-the-classic-notebook).
- \* `retro` is not installed at this time, but it could be the case in the future or in a community stack.
- Any other valid `jupyter` subcommand that starts the Jupyter Application can be used.
```

Example:

```bash
# Run Jupyter Server with the Jupyter Notebook frontend
docker run -it --rm \
    -p 8888:8888 \
    -e DOCKER_STACKS_JUPYTER_CMD=notebook \
    quay.io/jupyter/base-notebook
# Executing the command: jupyter notebook ...

# Use Jupyter NBClassic frontend
docker run -it --rm \
    -p 8888:8888 \
    -e DOCKER_STACKS_JUPYTER_CMD=nbclassic \
    quay.io/jupyter/base-notebook
# Executing the command: jupyter nbclassic ...
```

### `start.sh`

The `start-notebook.py` script inherits most of its option handling capability from a more generic `start.sh` script.
The `start.sh` script supports all the features described above but allows you to specify an arbitrary command to execute.
For example, to run the text-based `ipython` console in a container, do the following:

```bash
docker run -it --rm quay.io/jupyter/base-notebook start.sh ipython
```

This script is handy when you derive a new Dockerfile from this image and install additional Jupyter applications with subcommands like `jupyter console`, `jupyter kernelgateway`, etc.

### Others

You can bypass the provided scripts and specify an arbitrary start command.
If you do, keep in mind that features supported by the `start.sh` script and its kin will not function (e.g., `GRANT_SUDO`).

## Conda Environments

The default Python 3.x [Conda environment](https://conda.io/projects/conda/en/latest/user-guide/concepts/environments.html) resides in `/opt/conda`.
The `/opt/conda/bin` directory is part of the default `jovyan` user's `${PATH}`.
That directory is also searched for binaries when run using `sudo` (`sudo my_binary` will search for `my_binary` in `/opt/conda/bin/`

The `jovyan` user has full read/write access to the `/opt/conda` directory.
You can use either `mamba`, `pip` or `conda` (`mamba` is recommended) to install new packages without any additional permissions.

```bash
# install a package into the default (python 3.x) environment and cleanup it after
# the installation
mamba install --yes some-package && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

pip install --no-cache-dir some-package && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

conda install --yes some-package && \
    conda clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
```

### Using alternative channels

Conda is configured by default to use only the [`conda-forge`](https://anaconda.org/conda-forge) channel.
However, you can use alternative channels, either one-shot by overwriting the default channel in the installation command or by configuring `mamba` to use different channels.
The examples below show how to use the [anaconda default channels](https://repo.anaconda.com/pkgs/main) instead of `conda-forge` to install packages.

```bash
# using defaults channels to install a package
mamba install --channel defaults humanize

# configure conda to add default channels at the top of the list
conda config --system --prepend channels defaults

# install a package
mamba install --yes humanize && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
```

[switch_back]: #switching-back-to-the-classic-notebook-or-using-a-different-startup-command
