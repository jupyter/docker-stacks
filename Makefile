# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
.PHONY: docs help test

# Use bash for inline if-statements in arch_patch target
SHELL:=bash
OWNER?=jupyter

# Need to list the images in build dependency order
# All of the images
ALL_IMAGES:= \
	base-notebook \
	minimal-notebook \
	r-notebook \
	scipy-notebook \
	tensorflow-notebook \
	datascience-notebook \
	pyspark-notebook \
	all-spark-notebook

AARCH64_IMAGES:= \
	base-notebook \
	minimal-notebook \
	r-notebook \
	scipy-notebook \
	datascience-notebook \
	pyspark-notebook \
	all-spark-notebook

# Enable BuildKit for Docker build
export DOCKER_BUILDKIT:=1



# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@echo "jupyter/docker-stacks"
	@echo "====================="
	@echo "Replace % with a stack directory name (e.g., make build/minimal-notebook)"
	@echo
	@grep -E '^[a-zA-Z0-9_%/-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'



build/%: DOCKER_BUILD_ARGS?=
build/%: ## build the latest image for a stack using the system's architecture
	docker build $(DOCKER_BUILD_ARGS) --rm --force-rm -t $(OWNER)/$(notdir $@):latest ./$(notdir $@) --build-arg OWNER=$(OWNER)
	@echo -n "Built image size: "
	@docker images $(OWNER)/$(notdir $@):latest --format "{{.Size}}"
build-all: $(foreach I, $(ALL_IMAGES), build/$(I)) ## build all stacks
build-aarch64: $(foreach I, $(AARCH64_IMAGES), build/$(I)) ## build aarch64 stacks


check-outdated/%: ## check the outdated mamba/conda packages in a stack and produce a report (experimental)
	@TEST_IMAGE="$(OWNER)/$(notdir $@)" pytest tests/base-notebook/test_outdated.py
check-outdated-all: $(foreach I, $(ALL_IMAGES), check-outdated/$(I)) ## check all the stacks for outdated packages



cont-clean-all: cont-stop-all cont-rm-all ## clean all containers (stop + rm)
cont-stop-all: ## stop all containers
	@echo "Stopping all containers ..."
	-docker stop -t0 $(shell docker ps -a -q) 2> /dev/null
cont-rm-all: ## remove all containers
	@echo "Removing all containers ..."
	-docker rm --force $(shell docker ps -a -q) 2> /dev/null



docs: ## build HTML documentation
	sphinx-build -W --keep-going --color docs/ docs/_build/

linkcheck-docs: ## check broken links
	sphinx-build -W --keep-going --color -b linkcheck docs/ docs/_build/



hook/%: ## run post-build hooks for an image
	python3 -m tagging.tag_image --short-image-name "$(notdir $@)" --owner "$(OWNER)" && \
	python3 -m tagging.write_manifest --short-image-name "$(notdir $@)" --hist-line-dir /tmp/hist_lines/ --manifest-dir /tmp/manifests/ --owner "$(OWNER)"
hook-all: $(foreach I, $(ALL_IMAGES), hook/$(I)) ## run post-build hooks for all images



img-clean: img-rm-dang img-rm ## clean dangling and jupyter images
img-list: ## list jupyter images
	@echo "Listing $(OWNER) images ..."
	docker images "$(OWNER)/*"
img-rm: ## remove jupyter images
	@echo "Removing $(OWNER) images ..."
	-docker rmi --force $(shell docker images --quiet "$(OWNER)/*") 2> /dev/null
img-rm-dang: ## remove dangling images (tagged None)
	@echo "Removing dangling images ..."
	-docker rmi --force $(shell docker images -f "dangling=true" -q) 2> /dev/null



pre-commit-all: ## run pre-commit hook on all files
	@pre-commit run --all-files --hook-stage manual
pre-commit-install: ## set up the git hook scripts
	@pre-commit --version
	@pre-commit install



pull/%: ## pull a jupyter image
	docker pull $(OWNER)/$(notdir $@)
pull-all: $(foreach I, $(ALL_IMAGES), pull/$(I)) ## pull all images


push/%: ## push all tags for a jupyter image
	docker push --all-tags $(OWNER)/$(notdir $@)
push-all: $(foreach I, $(ALL_IMAGES), push/$(I)) ## push all tagged images



run-shell/%: ## run a bash in interactive mode in a stack
	docker run -it --rm $(OWNER)/$(notdir $@) $(SHELL)

run-sudo-shell/%: ## run a bash in interactive mode as root in a stack
	docker run -it --rm --user root $(OWNER)/$(notdir $@) $(SHELL)



test/%: ## run tests against a stack
	python3 -m tests.run_tests --short-image-name "$(notdir $@)" --owner "$(OWNER)"
test-all: $(foreach I, $(ALL_IMAGES), test/$(I)) ## test all stacks
