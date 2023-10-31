# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

.PHONY: help check image notebook

IMAGE:=my-notebook

# Common, extensible docker run command
define RUN_NOTEBOOK
@docker volume create --name $(WORK_VOLUME) > /dev/null
-@docker rm --force $(NAME) 2> /dev/null
@docker run --detach -p $(PORT):8888 \
	--name $(NAME) \
	-v $(WORK_VOLUME):/home/jovyan/work \
	$(DOCKER_ARGS) \
	$(IMAGE) bash -c "$(PRE_CMD) chown jovyan /home/jovyan/work && start-notebook.py $(ARGS)" > /dev/null
@echo "DONE: Notebook '$(NAME)' listening on $$(docker-machine ip $$(docker-machine active)):$(PORT)"
endef

help:
	@cat README.md

check:
	@which docker-machine > /dev/null || (echo "ERROR: docker-machine not found (brew install docker-machine)"; exit 1)
	@which docker > /dev/null || (echo "ERROR: docker not found (brew install docker)"; exit 1)
	@docker | grep volume > /dev/null || (echo "ERROR: docker 1.9.0+ required"; exit 1)

image: DOCKER_ARGS?=
image:
	@docker build --rm $(DOCKER_ARGS) --tag $(IMAGE) .

notebook: PORT?=80
notebook: NAME?=notebook
notebook: WORK_VOLUME?=$(NAME)-data
notebook: check
	$(RUN_NOTEBOOK)

# docker-machine drivers
include virtualbox.makefile
include softlayer.makefile

# Preset notebook configurations
include self-signed.makefile
include letsencrypt.makefile
