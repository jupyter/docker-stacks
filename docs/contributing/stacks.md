# Community Stacks

We love to see the community create and share new Jupyter Docker images. We've put together a [cookiecutter project](https://github.com/jupyter/cookiecutter-docker-stacks) and the documentation below to help you get started defining, building, and sharing your Jupyter environments in Docker. Following these steps will:

1. Setup a project on GitHub containing a Dockerfile based on either the `jupyter/base-notebook` or `jupyter/minimal-notebook` image.
2. Configure Travis CI to build and test your image when users submit pull requests to your repository.
3. Configure Docker Cloud to build and host your images for others to use.
4. Update the [list of community stacks](../using/selecting.html#community-stacks) in this documentation to include your image.

This approach mirrors how we build and share the core stack images. Feel free to follow it or pave your own path!

## Creating a Project

First, install [cookiecutter](https://github.com/audreyr/cookiecutter) using pip or conda:

```
pip install cookiecutter   # or conda install cookiecutter
```

Run the cookiecutter command pointing to the [jupyter/cookiecutter-docker-stacks](https://github.com/jupyter/cookiecutter-docker-stacks) project on GitHub.

```
cookiecutter https://github.com/jupyter/cookiecutter-docker-stacks.git
```

Enter a name for your new stack image. This will serve as both the git repository
name and the part of the Docker image name after the slash.

```
stack_name [my-jupyter-stack]:
```

Enter the user or organization name under which this stack will reside on
Docker Cloud / Hub. You must have access to manage this Docker Cloud org in
order to push images here and setup automated builds.

```
stack_org [my-project]:
```

Select an image from the jupyter/docker-stacks project that will serve as the
base for your new image.

```
stack_base_image [jupyter/base-notebook]:
```

Enter a longer description of the stack for your README.

```
stack_description [my-jupyter-stack is a community maintained Jupyter Docker Stack image]:
```

Initialize your project as a Git repository and push it to GitHub.

```
cd <stack_name you chose>

git init
git add .
git commit -m 'Seed repo'
git remote add origin <url from github>
git push -u origin master
```

## Configuring Travis

## Configuring Docker Cloud

## Sharing Your Image
