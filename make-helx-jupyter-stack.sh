#!/bin/bash

OWNER=containers.renci.org/helxplatform/jupyter/docker-stacks
DOCKER_BUILD_ARGS="--build-arg=NB_GID=0"
DOCKER_BUILD_ARGS+=" --build-arg=ROOT_CONTAINER=nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04"
export OWNER DOCKER_BUILD_ARGS

make "$@"