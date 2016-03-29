#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# The following can be overridden through environment variables.

# GitHub OAuth secrets
export GITHUB_CLIENT_ID="${GITHUB_CLIENT_ID:=}"
export GITHUB_CLIENT_SECRET="${GITHUB_CLIENT_SECRET:=}"
# OAuth callback URL, https://<jupyterhub.mydomain.com>/hub/oauth_callback
export OAUTH_CALLBACK_URL="${OAUTH_CALLBACK_URL:=}"

# Name of Docker overlay network
export DOCKER_NETWORK_NAME="${DOCKER_NETWORK_NAME:=jupyterhub-network}"

# Notebook server container image
export DOCKER_CONTAINER_IMAGE="${DOCKER_CONTAINER_IMAGE:=jupyter/singleuser:latest}"

# Machine name of the Swarm manager
export SWARM_MANAGER="${SWARM_MANAGER:=jupyterhub-manager}"
