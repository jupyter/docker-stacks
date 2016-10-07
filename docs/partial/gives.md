* Unprivileged user `jovyan` (uid=1000, configurable, see options) in group `users` (gid=100) with ownership over `/home/jovyan` and `/opt/conda`
* [tini](https://github.com/krallin/tini) as the container entrypoint and [start-notebook.sh]({{base_path}}/start-notebook.sh) as the default command
* A [start-singleuser.sh]({{base_path}}/start-singleuser.sh) script useful for running a single-user instance of the Notebook server, as required by JupyterHub
* A [start.sh]({{base_path}}/start.sh) script useful for running alternative commands in the container (e.g. `ipython`, `jupyter kernelgateway`, `jupyter lab`)
* Options for HTTPS, password auth, and passwordless `sudo`
