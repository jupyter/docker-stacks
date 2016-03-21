![docker pulls](https://img.shields.io/docker/pulls/jupyter/minimal-kernel.svg) ![docker stars](https://img.shields.io/docker/stars/jupyter/minimal-kernel.svg)

# Kernel Gateway Stack

## What it Gives You

* [Jupyter Kernel Gateway](https://github.com/jupyter-incubator/kernel_gateway) that enables programmatic access to kernels
* Python 3 kernel
* No preinstalled scientific computing packages
* [tini](https://github.com/krallin/tini) as the container entrypoint

## Basic Use

The following command starts a container with the Kernel Gateway server listening for HTTP connections on port 8888.

```
docker run -d -p 8888:8888 jupyter/minimal-kernel
```

## Docker Options and More Information
* For more information on the Kernel Gateway and its configuration options see the
[Kernel Gateway Repository](https://github.com/jupyter-incubator/kernel_gateway#what-it-gives-you).
