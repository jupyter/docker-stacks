# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
.PHONY: help test

# Use bash for inline if-statements in test target
SHELL:=bash
OWNER:=jupyter
ARCH:=$(shell uname -m)

# Need to list the images in build dependency order
ifeq ($(ARCH),ppc64le)
ALL_STACKS:=base-notebook
else
ALL_STACKS:=base-notebook \
	minimal-notebook \
	r-notebook \
	scipy-notebook \
	tensorflow-notebook \
	datascience-notebook \
	pyspark-notebook \
	all-spark-notebook
endif

ALL_IMAGES:=$(ALL_STACKS)

help:
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@echo "jupyter/docker-stacks"
	@echo "====================="
	@echo "Replace % with a stack directory name (e.g., make build/minimal-notebook)"
	@echo
	@grep -E '^[a-zA-Z0-9_%/-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

arch_patch/%: ## apply hardware architecture specific patches to the Dockerfile
	@if [ -e ./$(notdir $@)/Dockerfile.$(ARCH).patch ]; then \
		if [ -e ./$(notdir $@)/Dockerfile.orig ]; then \
               		cp -f ./$(notdir $@)/Dockerfile.orig ./$(notdir $@)/Dockerfile;\
		else\
                	cp -f ./$(notdir $@)/Dockerfile ./$(notdir $@)/Dockerfile.orig;\
		fi;\
		patch -f ./$(notdir $@)/Dockerfile ./$(notdir $@)/Dockerfile.$(ARCH).patch; \
	fi

build/%: DARGS?=
ifeq ($(GPU),1)
build/%: TAG_POSTFIX?=-gpu
build/%: BARGS?=--build-arg BASE=nvidia/cuda:8.0-cudnn7-devel-ubuntu16.04 --build-arg TAG_POSTFIX=$(TAG_POSTFIX)
endif
build/%: ## build the latest image for a stack
	docker build $(BARGS) $(DARGS) --rm --force-rm -t $(OWNER)/$(notdir $@):latest$(TAG_POSTFIX) ./$(notdir $@)

build-all: $(foreach I,$(ALL_IMAGES),arch_patch/$(I) build/$(I) ) ## build all stacks
build-test-all: $(foreach I,$(ALL_IMAGES),arch_patch/$(I) build/$(I) test/$(I) ) ## build and test all stacks

dev/%: ARGS?=
dev/%: DARGS?=
dev/%: PORT?=8888
dev/%: ## run a foreground container for a stack
	docker run -it --rm -p $(PORT):8888 $(DARGS) $(OWNER)/$(notdir $@) $(ARGS)

test-reqs: # install libraries required to run the integration tests
	pip install -r requirements-test.txt

test/%:
	@TEST_IMAGE="$(OWNER)/$(notdir $@)" pytest test

test/base-notebook: ## test supported options in the base notebook
	@TEST_IMAGE="$(OWNER)/$(notdir $@)" pytest test base-notebook/test