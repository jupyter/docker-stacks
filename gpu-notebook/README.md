# GPU-Notebook
#### Leverage Jupyter Notebooks with the power of your NVIDIA GPU and perform GPU calculations using Tensorflow and Pytorch in collaborative notebooks. 

![Jupyterlab Overview](/extra/jupyterlab-overview.png)

This notebook uses the robust toolstack of this project 
and the NVIDIA CUDA drivers as an alternatice basis 
to enable GPU calculations in the Jupyter notebooks.

## Contents

1. [Requirements](#requirements)
2. [Quickstart](#quickstart)
4. [Configuration](#configuration)


## Requirements

1.  Install [Docker](https://www.docker.com/community-edition#/download) version **1.10.0+**
3.  A NVIDIA GPU
3.  Get access to use your GPU via the CUDA drivers, 
    check out this medium [article](https://medium.com/@christoph.schranz/set-up-your-own-gpu-based-jupyterlab-e0d45fcacf43).
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
  
Afterwards, the image can be build and run using this command:
```bash
./run_Dockerfile.sh -p [port]:8888  
# where [port] is an integer with 4 or more digits, e.g.: 8888
```
This will run *GPU-Notebook* on [localhost:8888](http://localhost:8888) 
with the default password `asdf`. 

With these commands we can see if everything worked well:
```bash
docker ps
docker logs [service-name]
```

In order to stop the local deployment, run:

  ```bash
  docker rm -f [UID] 
  ```
 

## Configuration

Please set a new password using `gpu-notebook/jupyter_notebook_config.json`.
Therefore, hash your password in the form (password)(salt) using a sha1 hash generator, e.g., the sha1 generator of [sha1-online.com](http://www.sha1-online.com/). 
The input with the default password `asdf` is appended by a arbitrary salt `e49e73b0eb0e` to `asdfe49e73b0eb0e` and should yield the hash string as shown in the config below.
**Never give away your own unhashed password!**

Then update the config file as shown below and restart the service.

```json
{
  "NotebookApp": {
    "password": "sha1:e49e73b0eb0e:32edae7a5fd119045e699a0bd04f90819ca90cd6"
  }
}
```
