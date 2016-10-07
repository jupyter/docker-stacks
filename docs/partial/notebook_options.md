## Notebook Options

The Docker container executes a [`start-notebook.sh` script]({{base_path}}/start-notebook.sh) script by default. The `start-notebook.sh` script handles the `NB_UID` and `GRANT_SUDO` features documented in the next section, and then executes the `jupyter notebook`.

You can pass [Jupyter command line options](http://jupyter.readthedocs.org/en/latest/config.html#command-line-arguments) through the `start-notebook.sh` script when launching the container. For example, to secure the Notebook server with a password hashed using `IPython.lib.passwd()`, run the following:

```
docker run -d -p 8888:8888 jupyter/{{stack_name}} start-notebook.sh --NotebookApp.password='sha1:74ba40f8a388:c913541b7ee99d15d5ed31d4226bf7838f83a50e'
```

For example, to set the base URL of the notebook server, run the following:

```
docker run -d -p 8888:8888 jupyter/{{stack_name}} start-notebook.sh --NotebookApp.base_url=/some/path
```

You can sidestep the `start-notebook.sh` script and run your own commands in the container. See the *Alternative Commands* section later in this document for more information.
