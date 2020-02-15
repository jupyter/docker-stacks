#!/usr/bin/env bash
cd $(cd -P -- "$(dirname -- "$0")" && pwd -P)

# Set the path of the generated Dockerfile
export DOCKERFILE=".build/Dockerfile"

# Write the contents into the DOCKERFILE and start with the header
cat Dockerfile.header > $DOCKERFILE
cp jupyter_notebook_config.json .build/

echo "
############################################################################
#################### Dependency: jupyter/base-image ########################
############################################################################
" >> $DOCKERFILE
cat ../base-notebook/Dockerfile | grep -v BASE_CONTAINER >> $DOCKERFILE
cp ../base-notebook/fix-permissions .build/
cp ../base-notebook/jupyter_notebook_config.py .build/
cp ../base-notebook/start.sh .build/
cp ../base-notebook/start-notebook.sh .build/
cp ../base-notebook/start-singleuser.sh .build/

echo "
############################################################################
################# Dependency: jupyter/minimal-notebook #####################
############################################################################
" >> $DOCKERFILE
cat ../minimal-notebook/Dockerfile | grep -v BASE_CONTAINER >> $DOCKERFILE

echo "
############################################################################
################# Dependency: jupyter/scipy-notebook #######################
############################################################################
" >> $DOCKERFILE
cat ../scipy-notebook/Dockerfile | grep -v BASE_CONTAINER >> $DOCKERFILE

echo "
############################################################################
################ Dependency: jupyter/datascience-notebook ##################
############################################################################
" >> $DOCKERFILE
cat ../datascience-notebook/Dockerfile | grep -v BASE_CONTAINER >> $DOCKERFILE

echo "
############################################################################
################ Dependency: jupyter/tensorflow-notebook ##################
############################################################################
" >> $DOCKERFILE
cat ../tensorflow-notebook/Dockerfile | grep -v BASE_CONTAINER >> $DOCKERFILE

echo "
############################################################################
########################## Dependency: pytorch #############################
############################################################################
" >> $DOCKERFILE
cat Dockerfile.pytorch >> $DOCKERFILE


echo "
############################################################################
############################ Useful packages ###############################
############################################################################
" >> $DOCKERFILE
cat Dockerfile.usefulpackages >> $DOCKERFILE

echo "GPU Dockerfile was generated sucessfully in file $(pwd)/${DOCKERFILE}"
echo "Run 'bash run_Dockerfile.sh -p [PORT]' to start the GPU-based Juyterlab instance."
