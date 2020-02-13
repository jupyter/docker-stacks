# GPU-Jupyter
#### Leverage Jupyter Notebooks with the power of your NVIDIA GPU and perform GPU calculations using Tensorflow and Pytorch in collaborative notebooks. 

![Jupyterlab Overview](/extra/jupyterlab-overview.png)

First of all, thanks to [hub.docker.com/u/jupyter](https://hub.docker.com/u/jupyter) for creating and maintaining a robost  Python, R and Julia toolstack. This project uses their toolstack and uses the NVIDIA CUDA drivers as a basis to enable GPU calculations in the Jupyter notebooks.

## Contents

1. [Requirements](#requirements)
2. [Quickstart](#quickstart)
3. [Deployment](#deployment-in-the-docker-swarm)
4. [Configuration](#configuration)


## Requirements

1.  Install [Docker](https://www.docker.com/community-edition#/download) version **1.10.0+**
2.  Install [Docker Compose](https://docs.docker.com/compose/install/) version **1.6.0+**
3.  A NVIDIA GPU
3.  Get access to use your GPU via the CUDA drivers, check out this [medium](https://medium.com/@christoph.schranz/set-up-your-own-gpu-based-jupyterlab-e0d45fcacf43) article.
4.  Clone this repository
    ```bash
    git clone https://github.com/iot-salzburg/gpu-jupyter.git
    cd gpu-jupyter
    ```

## Quickstart

As soon as you have access to your GPU locally (it can be tested via a Tensorflow or PyTorch), you can run these commands to start the jupyter notebook via docker-compose:
  ```bash
  ./start-local.sh
  ```
  
This will run *GPU-Jupyter* by default on [localhost:8888](http://localhost:8888) with the default password `asdf`. The general usage is:
  ```bash
  ./start-local.sh -p [port:8888]  # port must be an integer with 4 or more digits.
  ```
  
With these commands we can see if everything worked well:
```bash
docker-compose ps
docker logs [service-name]
```

In order to stop the local deployment, run:

  ```bash
  ./stop-local.sh
  ```
 
 
 ## Deployment in the Docker Swarm
 
A Jupyter instance often requires data from other services. 
If that data-source is containerized in Docker and sharing a port for communication shouldn't be allowed, e.g., for security reasons,
then connecting the data-source with *GPU-Jupyter* within a Docker Swarm is a great option! \

### Set up Docker Swarm and Registry

This step requires a running [Docker Swarm](https://www.youtube.com/watch?v=x843GyFRIIY) on a cluster or at least on this node.
In order to register custom images in a local Docker Swarm cluster, 
a registry instance must be deployed in advance.
Note that the we are using the port 5001, as many services use the default port 5000.

```bash
sudo docker service create --name registry --publish published=5001,target=5000 registry:2
curl 127.0.0.1:5001/v2/
```
This should output `{}`. \

Afterwards, check if the registry service is available using `docker service ls`.


### Configure the shared Docker network

Additionally, *GPU-Jupyter* is connected to the data-source via the same *docker-network*. Therefore, This network must be set to **attachable** in the source's `docker-compose.yml`:

```yml
services:
  data-source-service:
  ...
      networks:
      - default
      - datastack
  ...
networks:
  datastack:
    driver: overlay
    attachable: true  
```
 In this example, 
 * the docker stack was deployed in Docker swarm with the name **elk** (`docker stack deploy ... elk`),
 * the docker network has the name **datastack** within the `docker-compose.yml` file,
 * this network is configured to be attachable in the `docker-compose.yml` file
 * and the docker network has the name **elk_datastack**, see the following output:
    ```bash
    sudo docker network ls
    # ...
    # [UID]        elk_datastack                   overlay             swarm
    # ...
    ```
  The docker network name **elk_datastack** is used in the next step as a parameter.
   
### Start GPU-Jupyter in Docker Swarm

Finally, *GPU-Jupyter* can be deployed in the Docker Swarm with the shared network, using:

```bash
./add-to-swarm.sh -p [port] -n [docker-network] -r [registry-port]
# e.g. ./add-to-swarm.sh -p 8848 -n elk_datastack -r 5001
```
where:
* **-p:** port specifies the port on which the service will be available.
* **-n:** docker-network is the name of the attachable network from the previous step, e.g., here it is **elk_datastack**.
* **-r:** registry port is the port that is published by the registry service, see [Set up Docker Swarm and Registry](set-up-docker-swarm-and-registry).

Now, *gpu-jupyter* will be accessable here on [localhost:8848](http://localhost:8848) with the default password `asdf` and shares the network with the other data-source, i.e., all ports of the data-source will be accessable within *GPU-Jupyter*, even if they aren't routed it the source's `docker-compose` file.

Check if everything works well using:
```bash
sudo docker service ps gpu_gpu-jupyter
docker service ps gpu_gpu-jupyter
```

In order to remove the service from the swarm, use:
```bash
./remove-from-swarm.sh
```

## Configuration

Please set a new password using `src/jupyter_notebook_config.json`.
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
