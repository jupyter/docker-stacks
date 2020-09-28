#!/bin/sh
# NOTE AWS profile must point to your DAIN credentials in your AWS configs
AWS_PROFILE="dain"
AWS_REGION="eu-central-1"
AWS_ECR_REPO="575790519909.dkr.ecr.${AWS_REGION}.amazonaws.com"
DOCKER_AWS_IMAGE="${AWS_ECR_REPO}/xai:latest"
# rebuild stack up to pytorch-notebook
make -j build-pytorch | tee pytorch-notebook.log
# login to DAIN AWS ECR repo
aws --profile $AWS_PROFILE ecr get-login-password --region $AWS_REGION | \
docker login --username AWS --password-stdin $AWS_ECR_REPO
# tag built image and push it to repo
docker tag dain/pytorch-notebook:latest $DOCKER_AWS_IMAGE
docker push $DOCKER_AWS_IMAGE