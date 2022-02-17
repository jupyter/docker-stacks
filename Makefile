# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
.PHONY: docs help test

# Use bash for inline if-statements in arch_patch target
SHELL:=bash
OWNER?=jupyter

# Need to list the images in build dependency order

# Images supporting the following architectures:
# - linux/amd64
# - linux/arm64
MULTI_IMAGES:= \
	base-notebook \
	minimal-notebook \
	r-notebook \
	scipy-notebook \
	pyspark-notebook \
	all-spark-notebook
# Images that can only be built on the amd64 architecture (aka. x86_64)
AMD64_ONLY_IMAGES:= \
	datascience-notebook \
	tensorflow-notebook
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

# Enable BuildKit for Docker build
export DOCKER_BUILDKIT:=1



# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@echo "jupyter/docker-stacks"
	@echo "====================="
	@echo "Replace % with a stack directory name (e.g., make build-multi/minimal-notebook)"
	@echo
	@grep -E '^[a-zA-Z0-9_%/-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'



build/%: DOCKER_BUILD_ARGS?=
build/%: ## build the latest image for a stack using the system's architecture
	@echo "::group::Build $(OWNER)/$(notdir $@) (system's architecture)"
	docker build $(DOCKER_BUILD_ARGS) --rm --force-rm -t $(OWNER)/$(notdir $@):latest ./$(notdir $@) --build-arg OWNER=$(OWNER)
	@echo -n "Built image size: "
	@docker images $(OWNER)/$(notdir $@):latest --format "{{.Size}}"
	@echo "::endgroup::"
build-all: $(foreach I, $(ALL_IMAGES), build/$(I)) ## build all stacks

# Limitations on docker buildx build (using docker/buildx 0.5.1):
#
# 1. Can't --load and --push at the same time
#
# 2. Can't --load multiple platforms
#
# What does it mean to --load?
#
# - It means that the built image can be referenced by `docker` CLI, for example
#   when using the `docker tag` or `docker push` commands.
#
# Workarounds due to limitations:
#
# 1. We always build a dedicated image using the current system architecture
#    named as OWNER/<stack>-notebook so we always can reference that image no
#    matter what during tests etc.
#
# 2. We always also build a multi-platform image during build-multi that will be
#    inaccessible with `docker tag` and `docker push` etc, but this will help us
#    test the build on the different platform and provide cached layers for
#    later.
#
# 3. We let push-multi refer to rebuilding a multi image with `--push`.
#
#    We can rely on the cached layer from build-multi now even though we never
#    tagged the multi image.
#
# Outcomes of the workaround:
#
# 1. We can keep using the previously defined Makefile commands that doesn't
#    include `-multi` suffix as before.
#
# 2. Assuming we have setup docker/dockerx properly to build in arm64
#    architectures as well, then we can build and publish such images via the
#    `-multi` suffix without needing a local registry.
#
# 3. If we get dedicated arm64 runners, we can test everything separately
#    without needing to update this Makefile, and if all tests succeeds we can
#    do a publish job that creates a multi-platform image for us.
#
build-multi/%: DOCKER_BUILD_ARGS?=
build-multi/%: ## build the latest image for a stack on both amd64 and arm64
	@echo "::group::Build $(OWNER)/$(notdir $@) (system's architecture)"
	docker buildx build $(DOCKER_BUILD_ARGS) -t $(OWNER)/$(notdir $@):latest ./$(notdir $@) --build-arg OWNER=$(OWNER) --load
	@echo -n "Built image size: "
	@docker images $(OWNER)/$(notdir $@):latest --format "{{.Size}}"
	@echo "::endgroup::"

	@echo "::group::Build $(OWNER)/$(notdir $@) (amd64,arm64)"
	docker buildx build $(DOCKER_BUILD_ARGS) -t build-multi-tmp-cache/$(notdir $@):latest ./$(notdir $@) --build-arg OWNER=$(OWNER) --platform "linux/amd64,linux/arm64"
	@echo "::endgroup::"
build-all-multi: $(foreach I, $(MULTI_IMAGES), build-multi/$(I)) $(foreach I, $(AMD64_ONLY_IMAGES), build/$(I)) ## build all stacks



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



dev/%: PORT?=8888
dev/%: ## run a foreground container for a stack
	docker run -it --rm -p $(PORT):8888 $(DARGS) $(OWNER)/$(notdir $@)

install-dev-env: ## install libraries required to build images and run tests
	@pip install -r requirements-dev.txt



docs: ## build HTML documentation
	sphinx-build -W --keep-going --color docs/ docs/_build/

linkcheck-docs: ## check broken links
	sphinx-build -W --keep-going --color -b linkcheck docs/ docs/_build/

install-docs-env: ## install libraries required to build docs
	@pip install -r requirements-docs.txt



hook/%: WIKI_PATH?=../wiki
hook/%: ## run post-build hooks for an image
	python3 -m tagging.tag_image --short-image-name "$(notdir $@)" --owner "$(OWNER)" && \
	python3 -m tagging.create_manifests --short-image-name "$(notdir $@)" --owner "$(OWNER)" --wiki-path "$(WIKI_PATH)"
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
	@pre-commit run --all-files || (printf "\n\n\n" && git --no-pager diff --color=always)
pre-commit-install: ## set up the git hook scripts
	@pre-commit --version
	@pre-commit install



pull/%: ## pull a jupyter image
	docker pull $(OWNER)/$(notdir $@)
pull-all: $(foreach I, $(ALL_IMAGES), pull/$(I)) ## pull all images


push/%: ## push all tags for a jupyter image
	@echo "::group::Push $(OWNER)/$(notdir $@) (system's architecture)"
	docker push --all-tags $(OWNER)/$(notdir $@)
	@echo "::endgroup::"
push-all: $(foreach I, $(ALL_IMAGES), push/$(I)) ## push all tagged images

push-multi/%: DOCKER_BUILD_ARGS?=
push-multi/%: ## push all tags for a jupyter image that support multiple architectures
	@echo "::group::Push $(OWNER)/$(notdir $@) (amd64,arm64)"
	docker buildx build $(DOCKER_BUILD_ARGS) $($(subst -,_,$(notdir $@))_EXTRA_TAG_ARGS) -t $(OWNER)/$(notdir $@):latest ./$(notdir $@) --build-arg OWNER=$(OWNER) --platform "linux/amd64,linux/arm64" --push
	@echo "::endgroup::"
push-all-multi: $(foreach I, $(MULTI_IMAGES), push-multi/$(I)) $(foreach I, $(AMD64_ONLY_IMAGES), push/$(I)) ## push all tagged images



run-shell/%: ## run a bash in interactive mode in a stack
	docker run -it --rm $(OWNER)/$(notdir $@) $(SHELL)

run-sudo-shell/%: ## run a bash in interactive mode as root in a stack
	docker run -it --rm --user root $(OWNER)/$(notdir $@) $(SHELL)



test/%: ## run tests against a stack
	@echo "::group::test/$(OWNER)/$(notdir $@)"
	tests/run_tests.py --short-image-name "$(notdir $@)" --owner "$(OWNER)"
	@echo "::endgroup::"
test-all: $(foreach I, $(ALL_IMAGES), test/$(I)) ## test all stacks
