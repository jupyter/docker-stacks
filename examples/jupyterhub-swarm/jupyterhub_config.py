# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

c = get_config()

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
# Spawn containers from this image
c.DockerSpawner.container_image = os.environ.get(
    'DOCKER_CONTAINER_IMAGE', 'jupyter/singleuser:latest'
)
# Connect containers to this Docker network
network_name = os.environ.get('DOCKER_NETWORK_NAME', 'jupyterhub-network')
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }
c.DockerSpawner.extra_start_kwargs = { 'network_mode': network_name }
# Mount username volume to notebook directory
c.DockerSpawner.volumes = { '{username}': '/home/jovyan/work' }
c.DockerSpawner.extra_create_kwargs = { 'volume_driver': 'convoy' }
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True
# Specify paths to certificate and key used to authenticate to remote Docker
# daemon (specified by DOCKER_HOST) over HTTPS
c.DockerSpawner.tls_cert = os.environ['DOCKER_TLS_CERT']
c.DockerSpawner.tls_key = os.environ['DOCKER_TLS_KEY']
# Do not provision user containers to the JupyterHub host
# c.DockerSpawner.environment = { 'constraint:node!=jupyterhub-manager': None }
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8080

# TLS config
c.JupyterHub.port = 443
c.JupyterHub.ssl_key = os.environ['SSL_KEY']
c.JupyterHub.ssl_cert = os.environ['SSL_CERT']

# authenticate users with GitHub OAuth
c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'
c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

# Store database on volume mounted inside container at DATA_VOLUME_MOUNT
data_dir = os.environ.get('DATA_VOLUME_MOUNT', '/data')
c.JupyterHub.db_url = 'sqlite:///{}/jupyterhub.sqlite'.format(data_dir)

# whitlelist allowed and admin users
c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = admin = set()
c.JupyterHub.admin_access = True
pwd = os.path.dirname(__file__)
with open(os.path.join(pwd, 'userlist')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        name = parts[0]
        whitelist.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)
