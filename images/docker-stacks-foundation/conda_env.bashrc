eval "$(conda shell.bash hook | sed 's/conda activate base//g')"
set +e
conda activate "${DOCKER_STACKS_CONDA_ENV}"
set -e
