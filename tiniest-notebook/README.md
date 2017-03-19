# Tiniest notebook stack #

This is the tiniest possible docker image that can run a Jupyter Notebook. It
is primarily meant for demo purposes where speed of pulling is important.

Not recommended for non-demo uses!

## What it gives you

It is based on [Alpine Linux](https://alpinelinux.org/). It uses pip to install
both the notebook and jupyterhub packages - the latter allows us to use this
image for single-user servers in Kubernetes / Docker spawners.

You can use pip3 to install packages (with `pip3` or `apk`) as root. There
are no non-root users provisioned.

## Basic usage

You can run a notebook with:

```
sudo docker run  -it  --rm  -p 8888:8888 jupyter/tiniest-notebook
```

The default command is `/usr/bin/jupyter` (not `/usr/local/bin/jupyth`). For
use with jupyterhub, `/usr/bin/jupyterhub-singleuser` is also available.
