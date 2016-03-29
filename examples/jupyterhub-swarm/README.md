This is an example of how to deploy [JupyterHub](https://github.com/jupyter/jupyterhub) on a multi-host cluster using [Docker Swarm](https://docs.docker.com/swarm/overview/).  The goal is to demonstrate how one can create a multi-user Jupyter notebook environment that can scale.  

This example:

* Runs JupyterHub in a Docker container
* Supports HTTPS connections using TLS certificate and keys from [Let's Encrypt](https://letsencrypt.org)
* Spawns single-user notebook servers in Docker containers using [DockerSpawner](https://github.com/jupyter/dockerspawner)
* Authenticates users using GitHub OAuth

This example uses Docker for all the things, including:

* [Docker Engine](https://docs.docker.com/engine/) 1.10.3+
* [Docker Machine](https://docs.docker.com/machine/) 0.6.0+ to create and manage Docker daemons on remote hosts
* [Docker Swarm](https://docs.docker.com/swarm/overview/) 1.1.3+ to deploy and manage a cluster of Docker daemons across multiple hosts
* [Docker Compose](https://docs.docker.com/compose/) 1.6.2+ to build and run containers on remote hosts

## Disclaimer

This example is **NOT** intended to represent a production deployment.  A production deployment would have a smaller attack surface and  high availability of each component.   For more information about deploying a production Swarm cluster, consult the [Swarm documentation](https://docs.docker.com/swarm/plan-for-production/).

## Topology

| Node                      | Name                                   |
| ------------------------- |:-------------------------------------- |
| Swarm manager             | `jupyterhub-manager`                   |
| Swarm node                | `jupyterhub-node0`, `jupyterhub-node1` |
| Discovery key-value store | `jupyterhub-keystore`                  |

TODO: image


## Prerequisites

*  This example assumes that you are using a local workstation/laptop to create and manage remote Docker hosts, and to build and deploy Docker containers on those hosts.  It requires [Docker Toolbox](https://www.docker.com/products/docker-toolbox) 1.10.3 or higher.  See the [installation instructions](https://docs.docker.com/engine/installation/) for your environment.
* This example deploys JupyterHub with TLS enabled (the default).  Only HTTPS connections are supported.  Therefore, you will also need:
  * a TLS certificate chain and key (instructions on how to obtain them are below if you do not already have them)
  * a registered, routable domain name, e.g, `jupyterhub.mydomain.com`.

## Setup machines

This example uses Docker Machine to create and manage remote Docker hosts.  It creates machines on [IBM SoftLayer](http://www.softlayer.com/).  It should be relatively straightforward to deploy machines to one of several other environments using Docker Machine's [supported drivers](https://docs.docker.com/machine/drivers/). To deploy to a different environment, modify the `DRIVER_OPTS` in the commands below.

```
# Set SoftLayer credentials
export SOFTLAYER_USER=<softlayer_user>
export SOFTLAYER_API_KEY=<softlayer_api_key>
```

### Setup a key-value store

```
# Create Docker machine
export DRIVER_OPTS="--driver softlayer \
  --softlayer-cpu 1 \
  --softlayer-memory 1024 \
  --softlayer-disk-size 25 \
  --softlayer-local-disk \
  --softlayer-domain cloudet.xyz \
  --softlayer-region wdc01"

docker-machine create $DRIVER_OPTS jupyterhub-keystore

# Activate machine
eval "$(docker-machine env jupyterhub-keystore)"

# Get the private IP of the machine
export CONSUL_IP=$(docker-machine ssh jupyterhub-keystore 'ifconfig eth0 | grep "inet addr:" | cut -d: -f2 | cut -d" " -f1')

# Start the consul container on the machine
docker-compose -f consul.yml up -d
```

### Create a Swarm cluster

Create a Swarm manager machine.  This host will run the JupyterHub hub and proxy services.  Docker Machine will create a Swarm cluster during this process.

```
# Communication with discovery keystore is over private network;
# CONSUL_IP is private IP address, which is eth0 on SoftLayer virtual devices
export SWARM_OPTS="--swarm-discovery consul://$CONSUL_IP:8500 \
  --engine-opt cluster-store=consul://$CONSUL_IP:8500 \
  --engine-opt cluster-advertise=eth0:2376"

# Create a Swarm manager
export DRIVER_OPTS="--driver softlayer \
  --softlayer-cpu 4 \
  --softlayer-memory 8192 \
  --softlayer-disk-size 100 \
  --softlayer-domain cloudet.xyz \
  --softlayer-region wdc01"

docker-machine create \
  $DRIVER_OPTS \
  --swarm --swarm-master \
  $SWARM_OPTS \
  jupyterhub-manager
```

Create two machines to join the Swarm cluster.  These hosts will run the single-user Jupyter notebook containers.  

```
# Create Swarm nodes
export DRIVER_OPTS="--driver softlayer \
  --softlayer-cpu 4 \
  --softlayer-memory 16384 \
  --softlayer-disk-size 100 \
  --softlayer-domain cloudet.xyz \
  --softlayer-region wdc01"

docker-machine create \
  $DRIVER_OPTS \
  --swarm \
  $SWARM_OPTS \
  jupyterhub-node0

docker-machine create \
  $DRIVER_OPTS \
  --swarm \
  $SWARM_OPTS \
  jupyterhub-node1
```

Verify the environment.  You should now have four machines.

```
docker-machine ls
NAME                  ACTIVE      DRIVER       STATE     URL                   SWARM                         DOCKER
jupyterhub-keystore   -           softlayer    Running   tcp://x.x.x.x:2376                                  v1.10.3   
jupyterhub-manager    * (swarm)   softlayer    Running   tcp://x.x.x.x:2376    jupyterhub-manager (master)   v1.10.3   
jupyterhub-node0      -           softlayer    Running   tcp://x.x.x.x:2376    jupyterhub-manager            v1.10.3   
jupyterhub-node1      -           softlayer    Running   tcp://x.x.x.x:2376    jupyterhub-manager            v1.10.3   
```

Docker Machine will deploy a Swarm manager container and a Swarm agent container to the Swarm manager host.  It will also deploy a Swarm agent container to each node.

```
# activate the Swarm manager
eval "$(docker-machine env --swarm jupyterhub-manager)"

# list all containers
docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
0218d807c775        swarm:latest        "/swarm join --advert"   2 hours ago         Up 2 hours                              jupyterhub-node1/swarm-agent
d2c67f79c1ce        swarm:latest        "/swarm join --advert"   2 hours ago         Up 2 hours                              jupyterhub-node0/swarm-agent
3b742451a6ff        swarm:latest        "/swarm join --advert"   2 hours ago         Up 2 hours                              jupyterhub-manager/swarm-agent
ed08053cdb1c        swarm:latest        "/swarm manage --tlsv"   2 hours ago         Up 2 hours                              jupyterhub-manager/swarm-agent-master
```

## Create an overlay network

Create an [overlay network](https://docs.docker.com/engine/userguide/networking/get-started-overlay/) that containers will use to communicate across hosts.  

Substitute your own value for `--subnet`.  Here we assign a private address space that does not interfere with others on our network.

```
# Activate Swarm manager node
eval "$(docker-machine env --swarm jupyterhub-manager)"

# Create an overlay network
docker network create --driver overlay --subnet=172.31.0.0/24 jupyterhub-network

docker network ls
...
NETWORK ID          NAME                        DRIVER
c942b45e80ad        jupyterhub-network          overlay             
...
```

Verify that each Swarm node has the new network.

```
eval "$(docker-machine env jupyterhub-manager)"
docker network ls
NETWORK ID          NAME                 DRIVER
c942b45e80ad        jupyterhub-network   overlay             

eval "$(docker-machine env jupyterhub-node0)"
docker network ls
NETWORK ID          NAME                 DRIVER
c942b45e80ad        jupyterhub-network   overlay             

eval "$(docker-machine env jupyterhub-node1)"
docker network ls
NETWORK ID          NAME                 DRIVER
c942b45e80ad        jupyterhub-network   overlay
```

The Docker infrastructure is now in place.

## Build JupyterHub

Configure JupyterHub and build it into a Docker image.

1. Get a TLS certificate chain from [Let's Encrypt](https://letsencrypt.org).  The `letsencrypt.sh` script runs a Docker container that creates a certificate chain and stores it on the container's host.  We activate the Swarm manager node before we run the script, since that's where we will deploy the JupyterHub container.  

	```
	# Activate the Swarm manager node
	eval "$(docker-machine env jupyterhub-manager)"

	# Run a letsencrypt container to generate certificate chain and private key
  # on the active machine
	FQDN=jupyterhub.mydomain.com EMAIL=me@somewhere.com ./letsencrypt.sh

  # Verify the secrets made it to the host
  docker-machine ssh jupyterhub-manager ls /etc/letsencrypt
	```

1. GitHub OAuth requires a registered application, so register JupyterHub as a [new application](https://github.com/settings/applications/new).

  The OAuth callback URL should be of the form:

	```
	https://<jupyterhub.mydomain.com>/hub/oauth_callback
	```

  You will need to pass the application client ID, client secret, and callback URL as environment variables when you run the JupyterHub container.  You can either set them in your shell, or add them to the `env.sh` script.

1. Create a `userlist` file.  This file is where we store authorized users.  The users should be GitHub handles.  For example, to create a single admin user:

	```
	cat << EOF > userlist
	jtyberg admin
	EOF
	```

1. Build the JupyterHub image on the Swarm manager node.  That's where we'll be running it.

	```
	eval "$(docker-machine env jupyterhub-manager)"

	./build.sh
	```

1. Pull the single-user Jupyter notebook container image to each Swarm node.  Even though the image would be pulled to the node when a new container is spawned on that node, JupyterHub may timeout if it's a big image, so it's better to do it beforehand.

  ```
  eval "$(docker-machine env --swarm jupyterhub-manager)"

  docker pull jupyter/singleuser:latest
  ```

## Run JupyterHub

Run the JupyterHub container on the Swarm.

```
eval "$(docker-machine env --swarm jupyterhub-manager)"

./hub.sh
```

## TODO

* Persistence!  Investigate [Flocker](https://docs.clusterhq.com/en/latest/docker-integration/tutorial-swarm-compose.html).
  * Single-user volumes.
  * Secrets/TLS certs.
  * `userlist`

* Separate the Docker host creation from the Swarm cluster creation.  There's a lot of magic happening when creating a Swarm-enabled Docker machine which will only lead to questions or confusion later.  For example, how does one restart the Swarm manager container if it goes down?  Wait, wut?  Exactly.

* Image cleanup / graceful shutdown.

## FAQ

1. How do I list nodes in my Swarm cluster?

  From any node on the cluster:

  ```
  docker run --rm -it swarm list consul://$CONSUL_IP:8500
  ```

1. How do I remove a node from my Swarm cluster?

	Heh.  Good one.  Options:

  * [Kill the swarm container and wait for TTL to expire](https://github.com/docker/swarm/issues/197)
  * [Consult the Docker Swarm docs?](https://github.com/docker/swarm/issues/1341)

## Troubleshooting

* I got this error when trying to start JupyterHub:

  ```
  ERROR: subnet sandbox join failed for "172.23.0.0/24": vxlan interface creation failed for subnet "172.23.0.0/24": failed to get link by name "vx-000100-eb611": Link not found
  ```

  See this [issue](https://github.com/docker/libnetwork/issues/945).  Workaround: restart each node in swarm cluster:

  ```
  docker-machine restart jupyterhub-nodeN
  ```

  The swarm containers should start after reboot.

## References

TODO: include these inline, where applicable.

* https://github.com/minrk/jupyterhub-demo
* https://docs.docker.com/engine/security/https/
