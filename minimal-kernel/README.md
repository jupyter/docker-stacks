# Kernel Gateway Stack

## What it Gives You
* [Jupyter Kernel Gateway](https://github.com/jupyter-incubator/kernel_gateway) that spawns minimal Jupyter Python kernel
* No preinstalled scientific computing packages
* Unprivileged user `jovyan` (uid=1000, configurable, see options) in group `users` (gid=100) with ownership over `/home/jovyan`
* [tini](https://github.com/krallin/tini) as the container entrypoint and [start.sh](./start.sh) as the default command
* Options for Port and Ip address


## Basic Use

The following command starts a container with the Kernel Gateway server listening for HTTP connections on port 8888.

```
docker run -d -p 8888:8888 jupyter/minimal-kernel
```

## Docker Options

You may customize the execution of the Docker container and the Notebook server it contains with the following optional arguments.

* `-e INTERFACE=10.10.10.10` - Configures Kernel Gateway to listen on the given interface. Defaults to '0.0.0.0', all interfaces, which is appropriate when running using default bridged Docker networking. When using Docker's `--net=host`, you may wish to use this option to specify a particular network interface.
* `-e PORT=8888` - Configures Kernel Gateway to listen on the given port. Defaults to 8888, which is the port exposed within the Dockerfile for the image. When using Docker's `--net=host`, you may wish to use this option to specify a particular port.