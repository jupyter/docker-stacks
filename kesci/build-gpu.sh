(cd .. && DARGS="--build-arg BASE_CONTAINER=nvidia/cuda:9.0-cudnn7-devel --build-arg NB_USER=kesci" make OWNER=klabteam build/base-notebook-gpu)
(cd .. && DARGS="--build-arg BASE_CONTAINER=klabteam/base-notebook-gpu --build-arg NB_USER=kesci" make OWNER=klabteam build/minimal-notebook-gpu)
(cd .. && DARGS="--build-arg BASE_CONTAINER=klabteam/minimal-notebook-gpu --build-arg NB_USER=kesci" make OWNER=klabteam build/scipy-notebook-gpu)
