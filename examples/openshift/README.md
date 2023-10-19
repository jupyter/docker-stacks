# OpenShift example

This example provides templates for deploying the Jupyter Project docker-stacks images to OpenShift.

## Prerequisites

Any OpenShift 3 environment.
The templates were tested with OpenShift 3.7.
It is believed they should work with at least OpenShift 3.6 or later.

Do be aware that the Jupyter Project docker-stacks images are very large.
The OpenShift environment you are using must provide sufficient quota on the per-user space for images and the file system for running containers.
If the quota is too small, the pulling of the images to a node in the OpenShift cluster when deploying them, will fail due to lack of space.
Even if the image is able to run, if the quota is only just larger than the space required for the image, you will not be able to install many packages into the container before running out of space.

OpenShift Online, the public hosted version of OpenShift from Red Hat has a quota of only 3GB for the image and container file system.
As a result, only the `minimal-notebook` can be started and there is little space remaining to install additional packages.
Although OpenShift Online is suitable for demonstrating these templates work, what you can do in that environment will be limited due to the size of the images.

If you want to experiment with using Jupyter Notebooks in an OpenShift environment, you should instead use [Minishift](https://www.openshift.org/minishift/).
Minishift provides you the ability to run OpenShift in a virtual machine on your own local computer.

## Loading the Templates

To load the templates, login to OpenShift from the command line and run:

```bash
oc create -f https://raw.githubusercontent.com/jupyter-on-openshift/docker-stacks/master/examples/openshift/templates.json
```

This should create the `jupyter-notebook` template

The template can be used from the command line using the `oc new-app` command, or from the OpenShift web console by selecting _Add to Project_.
This `README` is only going to explain deploying from the command line.

## Deploying a Notebook

To deploy a notebook from the command line using the template, run:

```bash
oc new-app --template jupyter-notebook
```

The output will be similar to:

```lang-none
--> Deploying template "jupyter/jupyter-notebook" to project jupyter

     Jupyter Notebook
     ---------
     Template for deploying Jupyter Notebook images.

     * With parameters:
        * APPLICATION_NAME=notebook
        * NOTEBOOK_IMAGE=docker.io/jupyter/minimal-notebook:latest
        * NOTEBOOK_PASSWORD=ded4d7cada554aa48e0db612e1ed1080 # generated

--> Creating resources ...
    configmap "notebook-cfg" created
    deploymentconfig "notebook" created
    route "notebook" created
    service "notebook" created
--> Success
    Access your application via route 'notebook-jupyter.b9ad.pro-us-east-1.openshiftapps.com'
    Run 'oc status' to view your app.
```

When no template parameters are provided, the name of the deployed notebook will be `notebook`.
The image used will be:

```lang-none
docker.io/jupyter/minimal-notebook:latest
```

A password you can use when accessing the notebook will be auto generated and is displayed in the output from running `oc new-app`.

To see the hostname for accessing the notebook run:

```bash
oc get routes
```

The output will be similar to:

```lang-none
NAME       HOST/PORT                                               PATH      SERVICES   PORT       TERMINATION     WILDCARD
notebook   notebook-jupyter.abcd.pro-us-east-1.openshiftapps.com             notebook   8888-tcp   edge/Redirect   None
```

A secure route will be used to expose the notebook outside the OpenShift cluster, so in this case the URL would be:

```lang-none
https://notebook-jupyter.abcd.pro-us-east-1.openshiftapps.com/
```

When prompted, enter the password for the notebook.

## Passing Template Parameters

To override the name for the notebook, the image used, and the password, you can pass template parameters using the `--param` option.

```bash
oc new-app --template jupyter-notebook \
    --param APPLICATION_NAME=mynotebook \
    --param NOTEBOOK_IMAGE=docker.io/jupyter/scipy-notebook:latest \
    --param NOTEBOOK_PASSWORD=mypassword
```

You can deploy any of the Jupyter Project docker-stacks images.

If you don't care what version of the image is used, add the `:latest` tag at the end of the image name, otherwise use the hash corresponding to the image version you want to use.

## Deleting the Notebook Instance

To delete the notebook instance, run `oc delete` using a label selector for the application name.

```bash
oc delete all,configmap --selector app=mynotebook
```

## Adding Persistent Storage

You can upload notebooks and other files using the web interface of the notebook.
Any uploaded files or changes you make to them will be lost when the notebook instance is restarted.
If you want to save your work, you need to add persistent storage to the notebook.
To add persistent storage run:

```bash
oc set volume dc/mynotebook --add \
    --type=pvc --claim-size=1Gi --claim-mode=ReadWriteOnce \
    --claim-name mynotebook-data --name data \
    --mount-path /home/jovyan
```

When you have deleted the notebook instance, if using a persistent volume, you will need to delete it in a separate step.

```bash
oc delete pvc/mynotebook-data
```

## Customizing the Configuration

If you want to set any custom configuration for the notebook, you can edit the config map created by the template.

```bash
oc edit configmap/mynotebook-cfg
```

The `data` field of the config map contains Python code used as the `jupyter_server_config.py` file.

If you are using a persistent volume, you can also create a configuration file at:

```lang-none
/home/jovyan/.jupyter/jupyter_server_config.py
```

This will be merged at the end of the configuration from the config map.

Because the configuration is Python code, ensure any indenting is correct.
Any errors in the configuration file will cause the notebook to fail when starting.

If the error is in the config map, edit it again to fix it and trigger a new deployment if necessary by running:

```bash
oc rollout latest dc/mynotebook
```

If you make an error in the configuration file stored in the persistent volume, you will need to scale down the notebook, so it isn't running.

```bash
oc scale dc/mynotebook --replicas 0
```

Then run:

```bash
oc debug dc/mynotebook
```

to run the notebook in debug mode.
This will provide you with an interactive terminal session inside a running container, but the notebook will not have been started.
Edit the configuration file in the volume to fix any errors and exit the terminal session.

Start up the notebook again.

```bash
oc scale dc/mynotebook --replicas 1
```

## Changing the Notebook Password

The password for the notebook is supplied as a template parameter, or if not supplied will be automatically generated by the template.
It will be passed into the container through an environment variable.

If you want to change the password, you can do so by editing the environment variable on the deployment configuration.

```bash
oc set env dc/mynotebook JUPYTER_NOTEBOOK_PASSWORD=mypassword
```

This will trigger a new deployment so ensure you have downloaded any work if not using a persistent volume.

If using a persistent volume, you could instead set up a password in the file `/home/jovyan/.jupyter/jupyter_server_config.py` as per guidelines in <https://jupyter-server.readthedocs.io/en/latest/operators/public-server.html>.

## Deploying from a Custom Image

If you want to deploy a custom variant of the Jupyter Project docker-stacks images, you can replace the image name with that of your own.
If the image is not stored on Docker Hub, but some other public image registry, prefix the name of the image with the image registry host details.

If the image is in your OpenShift project, because you imported the image into OpenShift, or used the docker build strategy of OpenShift to build a derived custom image,
you can use the name of the image stream for the image name, including any image tag if necessary.

This can be illustrated by first importing an image into the OpenShift project.

```bash
oc import-image docker.io/jupyter/datascience-notebook:latest --confirm
```

Then deploy it using the name of the image stream created.

```bash
oc new-app --template jupyter-notebook \
    --param APPLICATION_NAME=mynotebook \
    --param NOTEBOOK_IMAGE=datascience-notebook \
    --param NOTEBOOK_PASSWORD=mypassword
```

Importing an image into OpenShift before deploying it means that when a notebook is started, the image need only be pulled from the internal OpenShift image registry rather than Docker Hub for each deployment.
Because the images are so large, this can speed up deployments when the image hasn't previously been deployed to a node in the OpenShift cluster.
