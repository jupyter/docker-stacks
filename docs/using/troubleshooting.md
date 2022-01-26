# Troubleshooting Common Problems

When troubleshooting, you may see unexpected behaviors or receive an error message. This section provide links for identifying the cause of the problem and how to resolve it.

## Permission Issues

### Permission denied when mounting local folders

If you tried to start a Docker container while mounting a local volume and you get a `Permission denied` error:

* It is likely you are trying to start your container with a command similar to:

  ```bash
    docker run -it --rm \
        -p 8888:8888 \
        -v my-local-dir:/home/jovyan/work jupyter/datascience-notebook
  ```

Here are a few things you can try:

1. Use absolute paths when using the `-v` flag:

    ```bash
    -v $(pwd)/my-local-dir:/home/jovyan/work
    ```

2. Add the following arguments to your command:

  ```bash
    docker run -it --rm \
        -p 8888:8888 \
        -e NB_UID=1000 \
        -e CHOWN_HOME=yes \
        -v my-local-dir:/home/jovyan/work jupyter/datascience-notebook
  ```
