# Troubleshooting Common Problems

When troubleshooting, you may see unexpected behaviors or receive an error message. This section provides links for identifying the cause of the problem and how to resolve it.

## Permission Issues

### Permission denied when mounting local directories

If you are running a Docker container while mounting a local volume or host directory using the `-v` flag like so:

```bash
  docker run -it --rm \
      -v <local-dir>:/home/jovyan/work jupyter/datascience-notebook
```

you might face permissions issues when trying to access the mounted directory:

```bash
$ ls -l foo.txt
-rw-r--r-- 1 root root 0 Jan 131 10:36 foo.txt
$ echo hi > foo.txt
-bash: foo.txt: Permission denied
```

**Some things to try:**

1. Matching the container's UID/GID with the host's

   Docker handles mounting host directories differently to mounting volumes, even though the syntax is basically the same (i.e. `-v`).

   When you initialize a Docker container using the flag `-v` the host directories are bind mounted directly into the container.
   Therefore, the permissions and ownership are **exactly the same** as the ones in your local host (including user ids) which may result in permissions errors like the one displayed above.

   Suppose your local user has a `UID` of `1000`. To fix the UID discrepancies between your local directories and the container's
   directoriess, you need to set `NB_UID` and `NB_GID` to match the that of the local user:

   ```bash
     docker run -it --rm \
         -e NB_UID=1000 \
         -e NB_GID=1000 \
         --user root \
         -v <local-dir>:/home/jovyan/work jupyter/datascience-notebook
   ```

   Note that you need to use the flag `--user root` to ensure that the `UID` is updated at runtime.

   The caveat with this approach is that since these changes are applied at runtime, you will need to to re-run the same
   command with the appropriate flags and environment variables if you need to recreate the container.

**Other tips:**

- Use absolute paths when using the `-v` flag:

  ```bash
  -v $(PWD)/<local-dir>:/home/jovyan/work
  ```

  in this example, we use the syntax `$(PWD)` which will be replaced with the full path to the current directory. The destination path should also be an absolute path starting with a `/` such as `home/jovyan/work`.

- You might want to consider using the Docker native `--user <UID>` and `--group-add <GID>`:

  ```bash
  # note this will use the same UID from the user calling the command
  docker run -it --rm \
           --user "$(id -u)" --group-add users \ # $(id -u) prints the UID of the user that called docker run
           -v <local-dir>:/home/jovyan/work jupyter/datascience-notebook
  ```

  this command will not only launch the container with a specific user UID, but also add the that user to the `users` group so that it can modify the files in the default `/home` and `/opt/conda` directories.
