# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

.PHONY: help check image notebook secure-notebook

IMAGE:=my-notebook

# OK to re-run volume create, noop if volume already exists
# Destroy the old notebook container, consider it temporary
# Show the ports at the end
define RUN_NOTEBOOK
@docker volume create --name $(WORK_VOLUME) > /dev/null
-@docker rm -f $(NAME) 2> /dev/null
@docker run -d -p $(PORT):8888 \
		--name $(NAME) \
		-v $(WORK_VOLUME):/home/jovyan/work \
		$(DOCKER_ARGS) \
		$(IMAGE) bash -c "$(PRE_CMD) chown jovyan /home/jovyan/work && start-notebook.sh" > /dev/null
@echo "DONE: Notebook '$(NAME)' listening on $$(docker-machine ip $$(docker-machine active)):$(PORT)"
endef

help:
	@cat README.md

include virtualbox.makefile
include softlayer.makefile

check:
	@which docker-machine > /dev/null || (echo "ERROR: docker-machine not found (brew install docker-machine)"; exit 1)
	@which docker > /dev/null || (echo "ERROR: docker not found (brew install docker)"; exit 1)
	@docker | grep volume > /dev/null || (echo "ERROR: docker 1.9.0+ required"; exit 1)

image: DOCKER_ARGS?=
image:
	@docker build --rm $(DOCKER_ARGS) -t $(IMAGE) .

password-check:
	@test -n "$(PASSWORD)" || \
		(echo "ERROR: PASSWORD not defined or blank"; exit 1)

notebook: PORT?=80
notebook: NAME?=notebook
notebook: WORK_VOLUME?=$(NAME)-data
notebook: check
	$(RUN_NOTEBOOK)

secure-notebook: PORT?=443
secure-notebook: NAME?=notebook
secure-notebook: WORK_VOLUME?=$(NAME)-data
secure-notebook: SECRETS_VOLUME?=$(NAME)-secrets
secure-notebook: DOCKER_ARGS:=-e USE_HTTPS=yes \
	-e PASSWORD=$(PASSWORD) \
	-v $(NAME)-secrets:/home/jovyan/.local/share/jupyter
secure-notebook: PRE_CMD:=chown jovyan /home/jovyan/.local/share/jupyter;
secure-notebook: check password-check
	@docker volume create --name $(SECRETS_VOLUME) > /dev/null
	$(RUN_NOTEBOOK)
