## Docker Options

You may customize the execution of the Docker container and the command it is running with the following optional arguments.

* `-e PASSWORD="YOURPASS"` - Configures Jupyter Notebook to require the given plain-text password. Should be combined with `USE_HTTPS` on untrusted networks. **Note** that this option is not as secure as passing a pre-hashed password on the command line as shown above.
* `-e USE_HTTPS=yes` - Configures Jupyter Notebook to accept encrypted HTTPS connections. If a `pem` file containing a SSL certificate and key is not provided (see below), the container will generate a self-signed certificate for you.
* `-e NB_UID=1000` - Specify the uid of the `jovyan` user. Useful to mount host volumes with specific file ownership. For this option to take effect, you must run the container with `--user root`. (The `start-notebook.sh` script will `su jovyan` after adjusting the user id.)
* `-e GRANT_SUDO=yes` - Gives the `jovyan` user passwordless `sudo` capability. Useful for installing OS packages. For this option to take effect, you must run the container with `--user root`. (The `start-notebook.sh` script will `su jovyan` after adding `jovyan` to sudoers.) **You should only enable `sudo` if you trust the user or if the container is running on an isolated host.**
* `-v /some/host/folder/for/work:/home/jovyan/work` - Host mounts the default working directory on the host to preserve work even when the container is destroyed and recreated (e.g., during an upgrade).
* `-v /some/host/folder/for/server.pem:/home/jovyan/.local/share/jupyter/notebook.pem` - Mounts a SSL certificate plus key for `USE_HTTPS`. Useful if you have a real certificate for the domain under which you are running the Notebook server.
