eval "$(conda shell.bash hook | sed 's/conda activate base//g')"
conda activate "${DOCKER_STACKS_CONDA_ENV}"
