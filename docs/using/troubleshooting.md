# Troubleshooting Common Problems

When troubleshooting, you may see unexpected behaviors or receive an error message. This section provides advice on
how to identify and mitigate the cause of the problem and how to resolve it (for the most commonly encountered issues).

Most of the `docker run` flags used in this document are explained in detail in the [Common Features, Docker Options section](../using/common.html#Docker-Options) of the documentation.

## Permission denied when mounting volumes

If you are running a Docker container while mounting a local volume or host directory using the `-v` flag like so:

```bash
docker run -it --rm \
    -p 8888:8888 \
    -v <my-vol>:<container-dir> \
    jupyter/minimal-notebook:latest
```

you might face permissions issues when trying to access the mounted volume:

```bash
# assuming we mounted the volume in /home/jovyan/stagingarea
# root is the owner of the mounted volume
$ ls -ld ~/stagingarea/
drwxr-xr-x 2 root root 4096 Feb  1 12:55 stagingarea/

$ touch stagingarea/kale.txt
touch: cannot touch 'stagingarea/kale.txt': Permission denied
```

In this case the user of the container (`jovyan`) and the owner of the mounted volume (`root`) have different permission levels and ownership over the container's directories and mounts.
The following sections cover a few of these scenarios and suggestions to fix these problems.

**Some things to try:**

1. **Change ownership of the volume mount**

   You can change the ownership of the volume mount using the `chown` command. In the case of the docker-stacks images, you can set the `CHOWN_EXTRA` and `CHOWN_EXTRA_OPTS` environment variables.

   For example, to change the ownership of the volume mount to the jovyan user (non-privileged default user in the Docker images):

   ```bash
   # running in detached mode - can also be run in interactive mode
   docker run -d \
       -v <my-vol>:<container-dir> \
       -p 8888:8888 \
       --user root \
       -e CHOWN_EXTRA="<container-dir>" \
       -e CHOWN_EXTRA_OPTS="-R" \
       jupyter/minimal-notebook
   ```

   where:

   - `CHOWN_EXTRA=<some-dir>`: will change the ownership and group of the specified container directory (non-recursive by default). You need to provide full paths starting with `/`.
   - `CHOWN_EXTRA_OPTS="-R"`: will recursively change the ownership and group of the directory specified in `CHOWN_EXTRA`.
   - `--user root`: you **must** run the container with the root user to change ownership at runtime.

   now accessing the mount should work as expected:

   ```bash
   # assuming we mounted the volume in /home/jovyan/stagingarea
   $ ls -ld ~/stagingarea
   drwxr-xr-x 2 jovyan users 4096 Feb  1 12:55 stagingarea/

   $ touch stagingarea/kale.txt
   # jovyan is now the owner of /home/jovyan/stagingarea
   $ ls -la ~/stagingarea/
   -rw-r--r-- 1 jovyan users    0 Feb  1 14:41 kale.txt
   ```

   ```{admonition} Additional notes
      - If you are mounting your volume inside the `/home/` directory, you can use the `-e CHOWN_HOME=yes` and `CHOWN_HOME_OPTS="-R"` flags instead of the `-e CHOWN_EXTRA`
        and `-e CHOWN_EXTRA_OPTS` in the example above.
      - This solution should work in most cases where you have created a docker volume (i.e. using the [`docker volume create --name <my-volume>`
        command](https://docs.docker.com/storage/volumes/#create-and-manage-volumes)) and mounted it using the`-v` flag in `docker run`.
   ```

2. **Matching the container's UID/GID with the host's**

   Docker handles mounting host directories differently from mounting volumes, even though the syntax is essentially the same (i.e. `-v`).

   When you initialize a Docker container using the flag `-v`, the host directories are bind-mounted directly into the container.
   Therefore, the permissions and ownership are copied over and will be **the same** as the ones in your local host
   (including user ids) which may result in permissions errors when trying to access directories or create/modify files inside.

   Suppose your local user has a `UID` and `GID` of `1234`. To fix the UID discrepancies between your local directories and the container's
   directories, you can run the container with an explicit `NB_UID` and `NB_GID` to match the that of the local user:

   ```bash
   $ docker run -it --rm \
       --user root \
       -p 8888:8888 \
       -e NB_UID=1234 \
       -e NB_GID=1234 \
       -v $(PWD)/test:/home/jovyan/work \
       jupyter/minimal-notebook:latest

   # you should see an output similar to this
   Update jovyan's UID:GID to 1234:1234
   Running as jovyan: bash
   ```

   where:

   - `NB_IUD` and `NB_GID` should match the local user's UID and GID.
   - You must use `--user root` to ensure that the `UID` and `GID` are updated at runtime.

   ````{admonition} Additional notes
   - The caveat with this approach is that since these changes are applied at runtime, you will need to re-run the same command
     with the appropriate flags and environment variables if you need to recreate the container (i.e. after removing/destroying it).
   - If you pass a numeric UID, it must be in the range of 0-2147483647
   - This approach only updates the UID and GID of the **existing `jovyan` user** instead of creating a new user. From the above example:
     ```bash
     $ id
     uid=1234(jovyan) gid=1234(jovyan) groups=1234(jovyan),100(users)
   ````

## Permission issues after changing the UID/GIU and USER in the container

If on top of changing the UID and GID you also **need to create a new user**, you might be experiencing any of the following issues:

- `root` is the owner of `/home` or a mounted volume
- when starting the container, you get an error such as `Failed to change ownership of the home directory.`
- getting permission denied when trying to `conda install` packages

**Some things to try:**

1. **Ensure the new user has ownership of `/home` and volume mounts**

   For example, say you want to create a user `callisto` with a `GID` and `UID` of `1234`, you will have to add the following flags to the docker run command:

   ```bash
    docker run -it --rm \
        -p 8888:8888 \
        --user root \
        -e NB_USER=callisto \
        -e NB_UID=1234 \
        -e NB_GID=1234 \
        -e CHOWN_HOME=yes \
        -e CHOWN_HOME_OPTS="-R" \
        -w "/home/${NB_USER}" \
        -v $(PWD)/test:/home/callisto/work \
        jupyter/minimal-notebook

    # expected output
    Updated the jovyan user:
    - username: jovyan       -> callisto
    - home dir: /home/jovyan -> /home/callisto
    Update callisto's UID:GID to 1234:1234
    Attempting to copy /home/jovyan to /home/callisto...
    Success!
    Ensuring /home/callisto is owned by 1234:1234
    Running as callisto: bash
   ```

   where:

   - `-e NB_USER=callisto`: will create a new user `callisto` and automatically add it to the `users` group (does not delete jovyan)
   - `-e NB_UID=1234` and `-e NB_GID=1234`: will set the `UID` and `GID` of the new user (`callisto`) to `1234`
   - `-e CHOWN_HOME_OPTS="-R"` and `-e CHOWN_HOME=yes`: ensure that the new user is the owner of the `/home` directory and subdirectories
     (setting `CHOWN_HOME_OPTS="-R` will ensure this change is applied recursively)
   - `-w "/home/${NB_USER}"` sets the working directory to be the new user's home

   ```{admonition} Additional notes
    In the example above, the `-v` flag is used to mount the local volume onto the `/home` directory of the new user.

    However, if you are mounting a volume elsewhere, you also need to use the `-e CHOWN_EXTRA=<some-dir>` flag to avoid any permission
    issues (see the section [Permission denied when mounting volumes](../using/troubleshooting.html#permission-denied-when-mounting-volumes) in this page).
   ```

2. **Dynamically assign the user ID and GID**

   The above case ensures that the `/home` directory is owned by the a newly created user with an specific `UID` and `GID`, but if you want to assign the `UID` and `GID`
   of the new user dynamically you can make the following adjustments:

   ```bash
   docker run -it --rm \
       -p 8888:8888 \
       --user root \
       -e NB_USER=callisto \
       -e NB_UID="$(id -u)" \
       -e NB_GID="$(id -g)"  \
       -e CHOWN_HOME=yes \
       -e CHOWN_HOME_OPTS="-R" \
       -w "/home/${NB_USER}" \
       -v $(PWD)/test:/home/callisto/work \
       jupyter/minimal-notebook
   ```

   where:

   - `"$(id -u)" and "$(id -g)"` will dynamically assign the `UID` and `GID` of the user executing the `docker run` command to the new user (`callisto`)

## Additional tips and troubleshooting commands for permission-related errors

- Pass absolute paths to the `-v` flag:

  ```bash
  -v $(PWD)/<my-vol>:/home/jovyan/work
  ```

  In this example, we use the syntax `$(PWD)`, which is replaced with the full path to the current directory at runtime. The destination
  path should also be an absolute path starting with a `/` such as `home/jovyan/work`.

- You might want to consider using the Docker native `--user <UID>` and `--group-add users` flags instead of `-e NB_GID` and `-e NB_UID`:

  ```bash
  # note this will use the same UID from
  # the user calling the command, thus matching the local host

  docker run -it --rm \
      -p 8888:8888 \
      --user "$(id -u)" --group-add users \
      -v <my-vol>:/home/jovyan/work jupyter/datascience-notebook
  ```

  This command will launch the container with a specific user UID and add that user to the `users` group so that it can modify the files in the default `/home` and `/opt/conda` directories.
  Further avoiding issues when trying to `conda install` additional packages.

- Use `docker inspect <container_id>` and look for the [`Mounts` section](https://docs.docker.com/storage/volumes/#start-a-container-with-a-volume) to verify that the volume was created and mounted accordingly:

  ```json
  # for example, for a my-vol volume created with
  # docker volume create --name <my-vol>

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
    ],
  ```

## Tokens are being rejected

If you are a regular user of VSCode and the Jupyter extension you might experience either of these issues when using any of the docker-stacks images:

- using the produced token and/or URL results in an "Invalid credentials" error on the Jupyter "Token authentication is enabled" page
- when clicking on the URL displayed on your command line logs you face a "This site cannot be reached" page on your web browser

**Some things to try:**

1. The first thing you want to try is to check that there are no other Jupyter processes running in the background:

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

2. Alternatively - you might want to ensure that the "Jupyter: Auto Start" setting is turned off to avoid this issue in the future.

   You can achieve this from the `Preferences > Jupyter` menu in VScode:

   ![VSCode Preferences UI - Jupyter:Disable Jupyter Auto Start checkbox unchecked](../_static/using/troubleshooting/vscode-jupyter-settings.png)
