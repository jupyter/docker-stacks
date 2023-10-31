# Troubleshooting Common Problems

When troubleshooting, you may see unexpected behaviors or receive an error message.
This section provides advice on how to identify and fix some of the most commonly encountered issues.

Most of the `docker run` flags used in this document are explained in detail in the
[Common Features, Docker Options section](common.md#docker-options) of the documentation.

## Permission denied when mounting volumes

If you are running a Docker container while mounting a local volume or host directory using the `-v` flag like so:

```bash
docker run -it --rm \
    -p 8888:8888 \
    -v <my-vol>:<container-dir> \
    quay.io/jupyter/minimal-notebook:latest
```

you might face permissions issues when trying to access the mounted volume:

```bash
# assuming we mounted the volume in /home/jovyan/stagingarea
# root is the owner of the mounted volume
ls -ld ~/stagingarea/
# drwxr-xr-x 2 root root 4096 Feb  1 12:55 stagingarea/

touch stagingarea/kale.txt
# touch: cannot touch 'stagingarea/kale.txt': Permission denied
```

In this case, the user of the container (`jovyan`) and the owner of the mounted volume (`root`)
have different permission levels and ownership over the container's directories and mounts.
The following sections cover a few of these scenarios and how to fix them.

**Some things to try:**

1. **Change ownership of the volume mount**

   You can change the ownership of the volume mount using the `chown` command.
   In the case of the docker-stacks images, you can set the `CHOWN_EXTRA` and `CHOWN_EXTRA_OPTS` environment variables.

   For example, to change the ownership of the volume mount to the jovyan user (non-privileged default user in the Docker images):

   ```bash
   # running in detached mode - can also be run in interactive mode
   docker run --detach \
       -v <my-vol>:<container-dir> \
       -p 8888:8888 \
       --user root \
       -e CHOWN_EXTRA="<container-dir>" \
       -e CHOWN_EXTRA_OPTS="-R" \
       quay.io/jupyter/minimal-notebook
   ```

   where:

   - `CHOWN_EXTRA=<some-dir>,<some-other-dir>`: will change the ownership and group of the specified container directory (non-recursive by default).
     You need to provide full paths starting with `/`.
   - `CHOWN_EXTRA_OPTS="-R"`: will recursively change the ownership and group of the directory specified in `CHOWN_EXTRA`.
   - `--user root`: you **must** run the container with the root user to change ownership at runtime.

   Now accessing the mount should work as expected:

   ```bash
   # assuming we mounted the volume in /home/jovyan/stagingarea
   ls -ld ~/stagingarea
   # drwxr-xr-x 2 jovyan users 4096 Feb  1 12:55 stagingarea/

   touch stagingarea/kale.txt
   # jovyan is now the owner of /home/jovyan/stagingarea
   # ls -la ~/stagingarea/
   # -rw-r--r-- 1 jovyan users    0 Feb  1 14:41 kale.txt
   ```

   ```{admonition} Additional notes
      - If you are mounting your volume inside the `/home/` directory, you can use the `-e CHOWN_HOME=yes` and `CHOWN_HOME_OPTS="-R"` flags
      instead of the `-e CHOWN_EXTRA` and `-e CHOWN_EXTRA_OPTS` in the example above.
      - This solution should work in most cases where you have created a docker volume
      (i.e. using the [`docker volume create --name <my-volume>`command](https://docs.docker.com/storage/volumes/#create-and-manage-volumes)) and mounted it using the`-v` flag in `docker run`.
   ```

2. **Matching the container's UID/GID with the host's**

   Docker handles mounting host directories differently from mounting volumes, even though the syntax is essentially the same (i.e. `-v`).

   When you initialize a Docker container using the flag `-v`, the host directories are bind-mounted directly into the container.
   Therefore, the permissions and ownership are copied over and will be **the same** as the ones in your local host
   (including user ids) which may result in permissions errors when trying to access directories or create/modify files inside.

   Suppose your local user has a `UID` and `GID` of `1234` and `5678`, respectively.
   To fix the UID discrepancies between your local directories and the container's directories,
   you can run the container with an explicit `NB_UID` and `NB_GID` to match that of the local user:

   ```bash
   docker run -it --rm \
       --user root \
       -p 8888:8888 \
       -e NB_UID=1234 \
       -e NB_GID=5678 \
       -v "${PWD}"/test:/home/jovyan/work \
       quay.io/jupyter/minimal-notebook:latest

   # you should see an output similar to this
   # Update jovyan's UID:GID to 1234:5678
   # Running as jovyan: bash
   ```

   where:

   - `NB_IUD` and `NB_GID` should match the local user's UID and GID.
   - You **must** use `--user root` to ensure that the `UID` and `GID` are updated at runtime.

````{admonition} Additional notes
- The caveat with this approach is that since these changes are applied at runtime,
   you will need to re-run the same command with the appropriate flags and environment variables
   if you need to recreate the container (i.e. after removing/destroying it).
 - If you pass a numeric UID, it **must** be in the range of 0-2147483647
 - This approach only updates the UID and GID of the **existing `jovyan` user** instead of creating a new user.
   From the above example:
   ```bash
   id
   # uid=1234(jovyan) gid=5678(jovyan) groups=5678(jovyan),100(users)
   ```
````

## Permission issues after changing the UID/GID and USER in the container

If you have also **created a new user**, you might be experiencing any of the following issues:

- `root` is the owner of `/home` or a mounted volume
- when starting the container, you get an error such as `Failed to change ownership of the home directory.`
- getting permission denied when trying to `conda install` packages

**Some things to try:**

1. **Ensure the new user has ownership of `/home` and volume mounts**

   For example, say you want to create a user `callisto` with a `GID` and `UID` of `1234`.
   You will have to add the following flags to the docker run command:

   ```bash
    docker run -it --rm \
        -p 8888:8888 \
        --user root \
        -e NB_USER=callisto \
        -e NB_UID=1234 \
        -e NB_GID=1234 \
        -e CHOWN_HOME=yes \
        -e CHOWN_HOME_OPTS="-R" \
        -w "/home/callisto" \
        -v "${PWD}"/test:/home/callisto/work \
        quay.io/jupyter/minimal-notebook

    # Updated the jovyan user:
    # - username: jovyan       -> callisto
    # - home dir: /home/jovyan -> /home/callisto
    # Update callisto UID:GID to 1234:1234
    # Attempting to copy /home/jovyan to /home/callisto...
    # Success!
    # Ensuring /home/callisto is owned by 1234:1234
    # Running as callisto: bash
   ```

   where:

   - `-e NB_USER=callisto`: will create a new user `callisto` and automatically add it to the `users` group (does not delete jovyan)
   - `-e NB_UID=1234` and `-e NB_GID=1234`: will set the `UID` and `GID` of the new user (`callisto`) to `1234`
   - `-e CHOWN_HOME_OPTS="-R"` and `-e CHOWN_HOME=yes`: ensure that the new user is the owner of the `/home` directory and subdirectories
     (setting `CHOWN_HOME_OPTS="-R` will ensure this change is applied recursively)
   - `-w "/home/callisto"` sets the working directory to be the new user's home

   ```{admonition} Additional notes
    In the example above, the `-v` flag is used to mount the local volume onto the new user's `/home` directory.

    However, if you are mounting a volume elsewhere,
    you also need to use the `-e CHOWN_EXTRA=<some-dir>` flag to avoid any permission issues
    (see the section [Permission denied when mounting volumes](#permission-denied-when-mounting-volumes) on this page).
   ```

2. **Dynamically assign the user ID and GID**

   The above case ensures that the `/home` directory is owned by a newly created user with a specific `UID` and `GID`,
   but if you want to assign the `UID` and `GID` of the new user dynamically,
   you can make the following adjustments:

   ```bash
   docker run -it --rm \
       -p 8888:8888 \
       --user root \
       -e NB_USER=callisto \
       -e NB_UID="$(id -u)" \
       -e NB_GID="$(id -g)"  \
       -e CHOWN_HOME=yes \
       -e CHOWN_HOME_OPTS="-R" \
       -w "/home/callisto" \
       -v "${PWD}"/test:/home/callisto/work \
       quay.io/jupyter/minimal-notebook
   ```

   where:

   - `"$(id -u)" and "$(id -g)"` will dynamically assign the `UID` and `GID` of the user executing the `docker run` command to the new user (`callisto`)

## Additional tips and troubleshooting commands for permission-related errors

- Pass absolute paths to the `-v` flag:

  ```bash
  -v "${PWD}"/<my-vol>:/home/jovyan/work
  ```

  This example uses the syntax `${PWD}`, which is replaced with the full path to the current directory at runtime.
  The destination path should also be an absolute path starting with a `/` such as `/home/jovyan/work`.

- You might want to consider using the Docker native `--user <UID>` and `--group-add users` flags instead of `-e NB_UID` and `-e NB_GID`:

  ```bash
  # note this will use the same UID from
  # the user calling the command, thus matching the local host

  docker run -it --rm \
      -p 8888:8888 \
      --user "$(id -u)" --group-add users \
      -v <my-vol>:/home/jovyan/work quay.io/jupyter/datascience-notebook
  ```

  This command will launch the container with a specific user UID and add that user to the `users` group
  to modify the files in the default `/home` and `/opt/conda` directories.
  Further avoiding issues when trying to `conda install` additional packages.

- Use `docker inspect <container_id>` and look for the [`Mounts` section](https://docs.docker.com/storage/volumes/#start-a-container-with-a-volume)
  to verify that the volume was created and mounted accordingly:

  ```json
  {
    "Mounts": [
      {
        "Type": "volume",
        "Name": "my-vol",
        "Source": "/var/lib/docker/volumes/stagingarea/_data",
        "Destination": "/home/jovyan/stagingarea",
        "Driver": "local",
        "Mode": "z",
        "RW": true,
        "Propagation": ""
      }
    ]
  }
  ```

## Problems installing conda packages from specific channels

By default, the docker-stacks images have the conda channels priority set to `strict`.
This may cause problems when trying to install packages from a channel with lower priority.

```bash
conda config --show | grep priority
# channel_priority: strict

# to see its meaning
conda config --describe channel_priority

# checking the current channels
conda config --show default_channels
# default_channels:
# - https://repo.anaconda.com/pkgs/main
# - https://repo.anaconda.com/pkgs/r
```

**Installing packages from alternative channels:**

You can install packages from other conda channels (e.g. bioconda) by disabling the `channel_priority` setting:

```bash
# install by disabling channel priority at еру command level
conda install --no-channel-priority -c bioconda bioconductor-geoquery
```

Additional details are provided in the [Using alternative channels](../using/common.md#using-alternative-channels) section of the [Common features](common.md) page.

## Tokens are being rejected

If you are a regular user of VSCode and the Jupyter extension,
you might experience either of these issues when using any of the docker-stacks images:

- when clicking on the URL displayed on your command line logs, you face a "This site cannot be reached" page on your web browser
- using the produced token and/or URL results in an "Invalid credentials" error on the Jupyter "Token authentication is enabled" page

  ```bash
  # example log output from the docker run command

  # [...]
  # Or copy and paste one of these URLs:
  #   http://3d4cf3809e3f:8888/?token=996426e890f8dc22fa6835a44442b6026cba02ee61fee6a2
  #   or http://127.0.0.1:8888/?token=996426e890f8dc22fa6835a44442b6026cba02ee61fee6a2
  ```

**Some things to try:**

1. **Find lingering Jupyter processes in the background**

   The first thing you want to try is to check that no other Jupyter processes are running in the background:

   ```bash
   ps aux | grep jupyter
   ```

   If there are existing processes running, you can kill them with:

   ```bash
   # example output from the above command
   # my-user 3412 ... --daemon-module=vscode_datascience_helpers.jupyter_daemon

   # using the pid from the above log
   kill 3412
   ```

2. **Turn off Jupyter auto-start in VSCode**

   Alternatively - you might want to ensure that the `Jupyter: Disable Jupyter Auto Start` setting is turned on to avoid this issue in the future.

   You can achieve this from the `Settings > Jupyter` menu in VScode:

   ![VSCode Settings UI - Jupyter: Disable Jupyter Auto Start checkbox checked](../_static/using/troubleshooting/vscode-jupyter-settings.png)

3. **Route container to unused local port**

   Instead of mapping Docker port `8888` to local port `8888`, map to another unused local port.
   You can see an example of mapping to local port `8001`:

   ```bash
   docker run -it --rm -p 8001:8888 quay.io/jupyter/datascience-notebook
   ```

   When the terminal provides the link to access Jupyter: <http://127.0.0.1:8888/lab?token=80d45d241a1ba4c2...>,
   change the default port value of `8888` in the url to the port value mapped with the `docker run` command.

   In this example, we use 8001, so the edited link would be: <http://127.0.0.1:8001/lab?token=80d45d241a1ba4c2...>.

   Note: Port mapping for Jupyter has other applications outside of Docker.
   For example, it can be used to allow multiple Jupyter instances when using SSH to control cloud devices.
