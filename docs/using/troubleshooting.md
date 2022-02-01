# Troubleshooting Common Problems

When troubleshooting, you may see unexpected behaviors or receive an error message. This section provides links for identifying the cause of the problem and how to resolve it.

## Permission Issues

### Permission denied when mounting volumes

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
$ ls -ld ~/stagingarea/
drwxr-xr-x 2 root root 4096 Feb  1 12:55 stagingarea/

$ touch stagingarea/kale.txt
touch: cannot touch 'stagingarea/kale.txt': Permission denied
```

**Some things to try:**

1. **Change ownership of the volume mount**

   You can change the ownership of the volume mount using the `chown` command. For example, to change the ownership of the volume mount to the jovyan user:

   ```bash
   docker run -d \
       -v <my-vol>:<container-dir> \
       -p 8888:8888 \
       --user root \
       -e CHOWN_EXTRA="<container-dir>" \
       -e CHOWN_EXTRA_OPTS="-R" \
       jupyter/minimal-notebook
   ```

   where:

   - `CHOWN_EXTRA=<some-dir>`: will change the owner and group of the specified container directory (non recursive by default). You need to provide full paths starting with `/`.
   - `CHOWN_EXTRA_OPTS=R`: will recursively the owner and group of of the directory specified in `CHOWN_EXTRA`.
   - `--user root`: must run the container with the root user to perform the change of ownership.

   so now accessing the mount should work as expected:

   ```bash
   # assuming we mounted the volume in /home/jovyan/stagingarea
   $ ls -ld ~/stagingarea
   drwxr-xr-x 2 jovyan users 4096 Feb  1 12:55 stagingarea/

   $ touch stagingarea/kale.txt
   $ ls -la ~/stagingarea/
   -rw-r--r-- 1 jovyan users    0 Feb  1 14:41 kale.txt
   ```

   **Note**: If you are mounting your volume inside the `/home/` directory you can use the `-e CHOWN_HOME=yes` and `CHOWN_HOME_OPTS="-R"` flags instead of the
   `-e CHOWN_EXTRA` and `-e CHOWN_EXTRA_OPTS` in the example above.

2. **Matching the container's UID/GID with the host's**

   Docker handles mounting host directories differently to mounting volumes, even though the syntax is essentially the same (i.e. `-v`).

   When you initialize a Docker container using the flag `-v` the host directories are bind mounted directly into the container.
   Therefore, the permissions and ownership are copied over and will be **exactly the same** as the ones in your local host
   (including user ids) which may result in permissions errors like the one displayed above.

   Suppose your local user has a `UID` and `GID` of `1234`. To fix the UID discrepancies between your local directories and the container's
   directoriess, you need to set `NB_UID` and `NB_GID` to match the that of the local user:

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

   Some important things to notice:

   - You must use `--user root` to ensure that the `UID` is updated at runtime
   - The caveat with this approach is that since these changes are applied at runtime, you will need to to re-run the same command
     with the appropriate flags and environment variables if you need to recreate the container

     **Note** that this approach only updates the UID and GID of the existing jovyan user:

   ```bash
   $ id
   uid=1234(jovyan) gid=1234(jovyan) groups=1234(jovyan),100(users)
   ```

If on top of changing the UID and GID you also need to create a new user (and thus ensure this user has a home directory) you can use the following command:

```bash
 docker run -it --rm \
 --user root \
 -e NB_UID=1234 \
 -e NB_GID=1234 \
 -e NB_USER=trallard \
 -e CHOWN_HOME=yes \
 -e CHOWN_HOME_OPTS="-R" \
 -w "/home/${NB_USER}" \
 -v $(PWD)/test:/home/trallard/work \
  jupyter/minimal-notebook start.sh

 # expected output
 Updated the jovyan user:
 - username: jovyan       -> trallard
 - home dir: /home/jovyan -> /home/trallard
 Update trallard's UID:GID to 1234:1234
 Attempting to copy /home/jovyan to /home/trallard...
 Success!
 Ensuring /home/trallard is owned by 1234:1234
 Running as trallard: bash
```

**Additional tips and troubleshooting commands:**

- Use absolute paths when using the `-v` flag:

  ```bash
  -v $(PWD)/<my-vol>:/home/jovyan/work
  ```

  in this example, we use the syntax `$(PWD)` which will be replaced with the full path to the current directory. The destination path should also be an absolute path starting with a `/` such as `home/jovyan/work`.

- You might want to consider using the Docker native `--user <UID>` and `--group-add users` flags instead of `-e NB_GID` and `-e NB_UID`:

  ```bash
  # note this will use the same UID from
  # the user calling the command thus matching the local host

  docker run -it --rm \
      --user "$(id -u)" --group-add users \ # $(id -u) prints the UID of the user that called docker run
      -v <my-vol>:/home/jovyan/work jupyter/datascience-notebook
  ```

  this command will not only launch the container with a specific user UID, but also add the that user to the `users` group so that it can modify the files in the default `/home` and `/opt/conda` directories.
  Further avoiding issues when trying to `conda install` additional packages.

- Use `docker inspect <container_id>` and look for the [`Mounts` section](https://docs.docker.com/storage/volumes/#start-a-container-with-a-volume) to verify that the volume was created and mounted accordingly:

  ```json
  # for example for a my-vol volume created with docker volume create <my-vol>

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

<!-- When you chown a file to a particular user/group using the username or group name, chown will look in /etc/passwd for the username and /etc/group for the group to attempt to map the name to an ID. If the username / group name doesn't exist in those files, chown will fail.

docker run -it --rm \
  -p 8888:8888 \
  -v ~/Users/tania/docker-test:/home/jovyan/work jupyter/base-notebook \

  docker run -d \
  -p 8888:8888 \
  --name stagingtest \
  -v jupyter-staging:/home/jovyan/work \
  jupyter/base-notebook  -->
