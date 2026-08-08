# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
.PHONY: docs help

SHELL:=bash
REGISTRY?=quay.io
OWNER?=jupyter
# The full image reference, only used in the per-image targets, as it depends on the target name
IMG=$(REGISTRY)/$(OWNER)/$(notdir $@)

# Use Docker if available, otherwise use Apple's container framework
CONTAINER_CLI?=$(if $(shell command -v docker),docker,container)
ifeq ($(CONTAINER_CLI),docker)
	CONTAINER_NS:=docker container
	# Docker shows image sizes by default, Apple's container framework requires the flag
	IMAGE_LS_FLAGS:=
	# Docker prompts for confirmation without the flag, Apple's container framework never prompts
	IMAGE_PRUNE_FLAGS:=--force
	# Docker lists the image references directly, regardless of the table layout
	IMAGE_REFS:=docker image ls --format "{{.Repository}}:{{.Tag}}"
else
	CONTAINER_NS:=container
	IMAGE_LS_FLAGS:=--verbose
	IMAGE_PRUNE_FLAGS:=
	# Apple's container framework lists the image name and the tag in the first two columns
	IMAGE_REFS:=container image ls | awk 'NR > 1 { print $$1 ":" $$2 }'
endif

# List local image references (name:tag) matching the given pattern
define image_refs
$(IMAGE_REFS) | grep -E "$(1)" | grep -v "<none>"
endef

# IDs of all the containers, evaluated when a recipe uses it
ALL_CONTAINERS=$(shell $(CONTAINER_NS) ls --all --quiet)

# Enable BuildKit for Docker build
export DOCKER_BUILDKIT:=1

# All the images listed in the build dependency order
ALL_IMAGES:= \
	docker-stacks-foundation \
	base-notebook \
	minimal-notebook \
	scipy-notebook \
	r-notebook \
	julia-notebook \
	tensorflow-notebook \
	pytorch-notebook \
	datascience-notebook \
	pyspark-notebook \
	all-spark-notebook



# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@echo "jupyter/docker-stacks"
	@echo "====================="
	@echo "Replace % with a stack directory name (e.g., make build/minimal-notebook)"
	@echo "Container engine being used: $(CONTAINER_CLI) (override with CONTAINER_CLI=docker|container)"
	@echo
	@grep -E '^[a-zA-Z0-9_%/-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'



# Note that `ROOT_IMAGE` and `PYTHON_VERSION` arguments are only applicable to the `docker-stacks-foundation` image
build/%: DOCKER_BUILD_ARGS?=
# By default, use the sha-pinned root image from the Dockerfile stage
build/%: ROOT_IMAGE?=default_root_image
build/%: PYTHON_VERSION?=3.13
build/%: ## build the latest image for a stack using the system's architecture
	$(CONTAINER_CLI) build $(DOCKER_BUILD_ARGS) \
	  --tag "$(IMG)" \
	  "./images/$(notdir $@)" \
	  --build-arg REGISTRY="$(REGISTRY)" \
	  --build-arg OWNER="$(OWNER)" \
	  --build-arg ROOT_IMAGE="$(ROOT_IMAGE)" \
	  --build-arg PYTHON_VERSION="$(PYTHON_VERSION)"
	@$(CONTAINER_CLI) image ls $(IMAGE_LS_FLAGS) | grep -E "^(REPOSITORY|NAME|IMAGE)|^$(IMG)[: ]"
build-all: $(foreach I, $(ALL_IMAGES), build/$(I)) ## build all stacks



check-outdated/%: ## check the outdated mamba/conda packages in a stack and produce a report
	pytest tests/by_image/docker-stacks-foundation/test_outdated.py \
	  --registry "$(REGISTRY)" \
	  --owner "$(OWNER)" \
	  --image "$(notdir $@)"
check-outdated-all: $(foreach I, $(ALL_IMAGES), check-outdated/$(I)) ## check all the stacks for outdated packages



# `-t` means `--timeout` in Docker and `--time` in Apple's container framework
cont-stop-all: ## stop all containers
	@echo "Stopping all containers ..."
	$(if $(ALL_CONTAINERS),-$(CONTAINER_NS) stop -t 0 $(ALL_CONTAINERS))
cont-rm-all: ## remove all containers
	@echo "Removing all containers ..."
	$(if $(ALL_CONTAINERS),-$(CONTAINER_NS) rm --force $(ALL_CONTAINERS))
cont-clean-all: cont-stop-all cont-rm-all ## clean all containers (stop + rm)



docs: ## build HTML documentation
	sphinx-build -W --keep-going --color docs/ docs/_build/
linkcheck-docs: ## check for broken links
	sphinx-build -W --keep-going --color -b linkcheck docs/ docs/_build/



hook/%: VARIANT?=default
hook/%: REPOSITORY?=$(OWNER)/docker-stacks
hook/%: ## run post-build hooks for an image
	python3 -m tagging.apps.write_tags_file \
	  --registry "$(REGISTRY)" \
	  --owner "$(OWNER)" \
	  --image "$(notdir $@)" \
	  --variant "$(VARIANT)" \
	  --tags-dir /tmp/jupyter/tags/
	python3 -m tagging.apps.write_manifest \
	  --registry "$(REGISTRY)" \
	  --owner "$(OWNER)" \
	  --image "$(notdir $@)" \
	  --variant "$(VARIANT)" \
	  --hist-lines-dir /tmp/jupyter/hist_lines/ \
	  --manifests-dir /tmp/jupyter/manifests/ \
	  --repository "$(REPOSITORY)"
	python3 -m tagging.apps.apply_tags \
	  --registry "$(REGISTRY)" \
	  --owner "$(OWNER)" \
	  --image "$(notdir $@)" \
	  --variant "$(VARIANT)" \
	  --platform "$(shell uname -m)" \
	  --tags-dir /tmp/jupyter/tags/
hook-all: $(foreach I, $(ALL_IMAGES), hook/$(I)) ## run post-build hooks for all images



img-list: ## list jupyter images
	@echo "Listing $(OWNER) images ..."
	-$(CONTAINER_CLI) image ls $(IMAGE_LS_FLAGS) | grep -E "^(REPOSITORY|NAME|IMAGE)|(^|/)$(OWNER)/"
img-rm-dang: ## remove dangling images (tagged None)
	@echo "Removing dangling images ..."
	-$(CONTAINER_CLI) image prune $(IMAGE_PRUNE_FLAGS)
# The owner is matched as a path component, so that other owners like `jupyterhub` don't match
img-rm-jupyter: JUPYTER_IMAGES=$(shell $(call image_refs,(^|/)$(OWNER)/))
img-rm-jupyter: ## remove jupyter images
	@echo "Removing $(OWNER) images ..."
	$(if $(JUPYTER_IMAGES),-$(CONTAINER_CLI) image rm --force $(JUPYTER_IMAGES))
img-rm: img-rm-dang img-rm-jupyter ## remove dangling and jupyter images



pull/%: ## pull a jupyter image
	$(CONTAINER_CLI) image pull "$(IMG)"
pull-all: $(foreach I, $(ALL_IMAGES), pull/$(I)) ## pull all images
push/%: IMG_REFS=$(shell $(call image_refs,^$(IMG):))
push/%: ## push all tags for a jupyter image
	for ref in $(IMG_REFS); do $(CONTAINER_CLI) image push "$$ref"; done
push-all: $(foreach I, $(ALL_IMAGES), push/$(I)) ## push all tagged images



run-shell/%: ## run a bash in interactive mode in a stack
	$(CONTAINER_CLI) run -it --rm "$(IMG)" $(SHELL)
run-sudo-shell/%: ## run bash in interactive mode as root in a stack
	$(CONTAINER_CLI) run -it --rm --user root "$(IMG)" $(SHELL)



test/%: ## run tests against a stack
	python3 -m tests.run_tests \
	  --registry "$(REGISTRY)" \
	  --owner "$(OWNER)" \
	  --image "$(notdir $@)"
test-all: $(foreach I, $(ALL_IMAGES), test/$(I)) ## test all stacks
