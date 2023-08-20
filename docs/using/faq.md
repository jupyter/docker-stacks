# Frequently Asked Questions (FAQ)

## How to persist user data

There are 2 types of data, which you might want to persist.

1. If you want to persist your environment (i.e. packages installed by `mamba`, `conda`, `pip`, `apt-get` and so on),
   then you should create an inherited image and install them only once while building your Dockerfile.
   An example for using `mamba` and `pip` in a child image is available
   [here](./recipes.md#using-mamba-install-recommended-or-pip-install-in-a-child-docker-image).

   ```{note}
   If you install a package inside a running container (for example you run `pip install <package>` in a terminal),
   it won't be preserved when you next run your image.
   To make it work, install this package in your inherited image and rerun `docker build` command.
   ```

2. If you want to persist user-data (files created by you, like `python` scripts, notebooks, text files and so on),
   then you should use a
   [Docker bind mount](https://docs.docker.com/storage/bind-mounts/) or
   [Docker Volume](https://docs.docker.com/storage/volumes/).
   You can find [an example of using bind mount here](./running.md#example-2).
   There is also [a mount troubleshooting section](./troubleshooting.md#permission-denied-when-mounting-volumes) if you experience any issues.

## Why we do not add your favorite package

We have lots of users with different packages they want to use.
Adding them all is impossible, so we have several images to choose from.
[Choose the image](selecting.md), that is closest to your needs and feel free to [add your package on top of our images](recipes.md#using-mamba-install-recommended-or-pip-install-in-a-child-docker-image).

## Who is `jovyan`

As described [here](https://github.com/jupyter/docker-stacks/issues/358#issuecomment-288844834):

```text
Jo·vy·an
/ˈjōvēən/
noun – an inhabitant of Jupyter
```

`Jovyan` is often a special term used to describe members of the Jupyter community.
It is also used as the user ID in the Jupyter Docker stacks or referenced in conversations.
You can find more information [here](https://docs.jupyter.org/en/latest/community/content-community.html#what-is-a-jovyan).

## How to give root permissions to the user

We have a [recipe for enabling root permissions](recipes.md#using-sudo-within-a-container).
