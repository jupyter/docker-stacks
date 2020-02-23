# GPU-Notebook
#### Leverage Jupyter Notebooks with the power of your NVIDIA GPU and perform GPU calculations using Tensorflow and Pytorch in collaborative notebooks. 

![Jupyterlab Overview](/gpu-notebook/extra/jupyterlab-overview.png)

This notebook uses the robust toolstack of this project 
and the NVIDIA CUDA drivers as an alternatice basis 
to enable GPU calculations in the Jupyter notebooks.

## Contents

1. [Requirements](#requirements)
2. [Quickstart](#quickstart)
3. [Tracing](#tracing)
5. [Configuration](#configuration)


## Requirements

1.  Install [Docker](https://www.docker.com/community-edition#/download) version **1.10.0+**
 and [Docker Compose](https://docs.docker.com/compose/install/) version **1.6.0+**.
2.  A NVIDIA GPU
3.  Get access to use your GPU via the CUDA drivers, check out this 
[medium article](https://medium.com/@christoph.schranz/set-up-your-own-gpu-based-jupyterlab-e0d45fcacf43).
    The CUDA toolkit is not required on the host system, as it will be deployed 
    in [NVIDIA-docker](https://github.com/NVIDIA/nvidia-docker).
4.  Clone this repository
    ```bash
    git clone https://github.com/ChristophSchranz/docker-stacks.git
    cd docker-stacks/gpu-notebook
    ```

## Quickstart

As soon as you have access to your GPU locally 
(it can be tested via a Tensorflow or PyTorch), 
you can generate a new `Dockerfile`, that pulls a basic `CUDA` version 
and then appends the installation steps from the following images of this project:

* jupyter/base-image
* jupyter/minimal-notebook
* jupyter/scipy-notebook
* jupyter/datascience-notebook
* jupyter/tensorflow-notebook

Finally, `PyTorch` and some other useful packages are installed, 
as defined in `Dockerfile.pytorch` and `Dockerfile.usefulpackages`.

To generate the comprehensive Dockerfile as `gpu-notebook/.build/Dockerfile`, run:

```bash
./generate_Dockerfile.sh
```

If the latest version of the build should be used, a `git pull`
is recommended before the generation of the Dockerfile. 
This step may result in rebuilding the whole image which can take some time.

Finally, the image can be build and run using this command:
```bash
docker build -t gpu-jupyter .build/
docker run -d -p [port]:8888 gpu-jupyter
``` 

Alternatively, you can configure the environment in `docker-compose.yml` and run 
this to deploy the `GPU-Jupyter` via docker-compose (under-the-hood):

```bash
./generate_Dockerfile.sh
./start-local.sh -p 8888  # where -p stands for the port of the service
```
  
Both options will run *GPU-Jupyter* by default on [localhost:8888](http://localhost:8888) with the default 
password `asdf`.


## Tracing
  
With these commands we can see if everything worked well:
```bash
docker ps
docker logs [service-name]
```

In order to stop the local deployment, run:

  ```bash
  ./stop-local.sh
  ```
 
 

## Configuration

Please set a new password using `gpu-notebook/jupyter_notebook_config.json`.
Therefore, hash your password in the form (password)(salt) using a sha1 hash generator, e.g., the sha1 generator of [sha1-online.com](http://www.sha1-online.com/). 
The input with the default password `asdf` is appended by a arbitrary salt `e49e73b0eb0e` to `asdfe49e73b0eb0e` and should yield the hash string as shown in the config below.
**Please change the default password immediately and never give away your own unhashed password!**

Then update the config file as shown below and restart the service.

```json
{
  "NotebookApp": {
    "password": "sha1:e49e73b0eb0e:32edae7a5fd119045e699a0bd04f90819ca90cd6"
  }
}
```

### Update CUDA to another version

To update CUDA to another version, change in `Dockerfile.header`
the line:

    FROM nvidia/cuda:10.1-base-ubuntu18.04
    
and in the `Dockerfile.pytorch` the line:

    cudatoolkit=10.1

Then re-generate and re-run the image, as closer described above:

```bash
./generate_Dockerfile.sh
./run_Dockerfile.sh -p [port]:8888  
```
