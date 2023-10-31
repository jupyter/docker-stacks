# Custom Jupyter Notebook images

This example provides scripts for building custom Jupyter Notebook images containing notebooks, data files, and with Python packages required by the notebooks already installed.
The scripts provided work with the Source-to-Image tool, and you can create the images from the command line on your own computer.
Templates are also provided to enable running builds in OpenShift, as well as deploying the resulting image to OpenShift to make it available.

The build scripts, when used with the Source-to-Image tool, provide similar capabilities to `repo2docker`.
When builds are run under OpenShift with the supplied templates, it provides similar capabilities to `mybinder.org`,
but where notebook instances are deployed in your existing OpenShift project and JupyterHub is not required.

For separate examples of using JupyterHub with OpenShift, see the project:

- <https://github.com/jupyter-on-openshift/jupyterhub-quickstart>

## Source-to-Image Project

Source-to-Image (S2I) is an open source project which provides a tool for creating container images.
It works by taking a base image, injecting additional source code or files into a running container created from the base image,
and running a builder script in the container to process the source code or files to prepare the new image.

Details on the S2I tool, and executable binaries for Linux, macOS and Windows, can be found on GitHub at:

- <https://github.com/openshift/source-to-image>

The tool is standalone, and can be used on any system which provides a docker daemon for running containers.
To provide an end-to-end capability to build and deploy applications in containers, support for S2I is also integrated into container platforms such as OpenShift.

## Getting Started with S2I

As an example of how S2I can be used to create a custom image with a bundled set of notebooks, run:

```bash
s2i build \
    --scripts-url https://raw.githubusercontent.com/jupyter/docker-stacks/main/examples/source-to-image \
    --context-dir docs/source/examples/Notebook \
    https://github.com/jupyter/notebook \
    docker.io/jupyter/minimal-notebook:latest \
    notebook-examples
```

This example command will pull down the Git repository <https://github.com/jupyter/notebook>
and build the image `notebook-examples` using the files contained in the `docs/source/examples/Notebook` directory of that Git repository.
The base image which the files will be combined with is `docker.io/jupyter/minimal-notebook:latest`, but you can specify any of the Jupyter Project `docker-stacks` images as the base image.

The resulting image from running the command can be seen by running `docker images` command:

```bash
docker images
# REPOSITORY         TAG     IMAGE ID      CREATED        SIZE
# notebook-examples  latest  f5899ed1241d  2 minutes ago  2.59GB
```

You can now run the image.

```bash
docker run --rm -p 8888:8888 notebook-examples
```

Open your browser on the URL displayed, and you will find the notebooks from the Git repository and can work with them.

## The S2I Builder Scripts

Normally when using S2I, the base image would be S2I enabled and contain the builder scripts needed to prepare the image and define how the application in the image should be run.
As the Jupyter Project `docker-stacks` images are not S2I enabled (although they could be),
in the above example the `--scripts-url` option has been used to specify that the example builder scripts contained in this directory of this Git repository should be used.

Using the `--scripts-url` option, the builder scripts can be hosted on any HTTP server,
or you could also use builder scripts local to your computer file using an appropriate `file://` format URI argument to `--scripts-url`.

The builder scripts in this directory of this repository are `assemble` and `run` and are provided as examples of what can be done.
You can use the scripts as is, or create your own.

The supplied `assemble` script performs a few key steps.

The first steps copy files into the location they need to be when the image is run, from the directory where they are initially placed by the `s2i` command.

```bash
cp -Rf /tmp/src/. "/home/${NB_USER}"

rm -rf /tmp/src
```

The next steps are:

```bash
if [ -f "/home/${NB_USER}/environment.yml" ]; then
    mamba env update --name root --file "/home/${NB_USER}/environment.yml"
    mamba clean --all -f -y
else
    if [ -f "/home/${NB_USER}/requirements.txt" ]; then
        pip --no-cache-dir install -r "/home/${NB_USER}/requirements.txt"
    fi
fi
```

This determines whether a `environment.yml` or `requirements.txt` file exists with the files and if so, runs the appropriate package management tool to install any Python packages listed in those files.

This means that so long as a set of notebook files provides one of these files listing what Python packages they need,
those packages will be automatically installed into the image, so they are available when the image is run.

A final step is:

```bash
fix-permissions "${CONDA_DIR}"
fix-permissions "/home/${NB_USER}"
```

This fixes up permissions on any new files created by the build.
This is necessary to ensure that when the image is run, you can still install additional files.
This is important for when an image is run in `sudo` mode, or it is hosted in a more secure container platform such as Kubernetes/OpenShift where it will be run as a set user ID that isn't known in advance.

As long as you preserve the first and last set of steps, you can do whatever you want in the `assemble` script to install packages, create files etc.
Do be aware though that S2I builds do not run as `root` and so you cannot install additional system packages.
If you need to install additional system packages, use a `Dockerfile` and normal `docker build` to first create a new custom base image from the Jupyter Project `docker-stacks` images,
with the extra system packages, and then use that image with the S2I build to combine your notebooks and have Python packages installed.

The `run` script in this directory is very simple and just runs the notebook application.

```bash
exec start-notebook.py "$@"
```

## Integration with OpenShift

The OpenShift platform provides integrated support for S2I type builds.
Templates are provided for using the S2I build mechanism with the scripts in this directory.
To load the templates run:

```bash
oc create -f https://raw.githubusercontent.com/jupyter/docker-stacks/main/examples/source-to-image/templates.json
```

This will create the templates:

```bash
jupyter-notebook-builder
jupyter-notebook-quickstart
```

The templates can be used from the OpenShift web console or command line.
This `README` is only going to explain deploying from the command line.

To use the OpenShift command line to build into an image, and deploy, the set of notebooks used above, run:

```bash
oc new-app --template jupyter-notebook-quickstart \
    --param APPLICATION_NAME=notebook-examples \
    --param GIT_REPOSITORY_URL=https://github.com/jupyter/notebook \
    --param CONTEXT_DIR=docs/source/examples/Notebook \
    --param BUILDER_IMAGE=docker.io/jupyter/minimal-notebook:latest \
    --param NOTEBOOK_PASSWORD=mypassword
```

You can provide a password using the `NOTEBOOK_PASSWORD` parameter.
If you don't set that parameter, a password will be generated, with it being displayed by the `oc new-app` command.

Once the image has been built, it will be deployed.
To see the hostname for accessing the notebook, run `oc get routes`.

```lang-none
NAME                HOST/PORT                                                       PATH SERVICES           PORT      TERMINATION    WILDCARD
notebook-examples   notebook-examples-jupyter.abcd.pro-us-east-1.openshiftapps.com       notebook-examples  8888-tcp  edge/Redirect  None
```

As the deployment will use a secure connection, the URL for accessing the notebook in this case would be <https://notebook-examples-jupyter.abcd.pro-us-east-1.openshiftapps.com>.

If you only want to build an image but not deploy it, you can use the `jupyter-notebook-builder` template.
You can then deploy it using the `jupyter-notebook` template provided with the [openshift](../openshift) examples directory.

See the `openshift` examples directory for further information on customizing configuration for a Jupyter Notebook deployment and deleting a deployment.
