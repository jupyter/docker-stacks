# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Use bash for inline if-statements in test target
SHELL:=bash
# Project name
OWNER:=jupyter
# Target architecture
ARCH:=$(shell uname -m)
# Order of image builds
ifeq ($(ARCH),ppc64le)
ALL_IMAGES:=base-notebook
else
ALL_IMAGES:=base-notebook \
	minimal-notebook \
	r-notebook \
	scipy-notebook \
	tensorflow-notebook \
	datascience-notebook \
	pyspark-notebook \
	all-spark-notebook
endif
# Current git commit SHA, used to tag release images
GIT_MASTER_HEAD_SHA:=$(shell git rev-parse --short=12 --verify HEAD)
# Number of retries when using the retry/* target prefix
RETRIES:=10
# Where to cache docker images between CI runs
CACHE_DIR?=.cache

help:
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@echo "jupyter/docker-stacks"
	@echo "====================="
	@echo "Replace % with a stack directory name (e.g., make build/minimal-notebook)"
	@echo
	@grep -E '^[a-zA-Z0-9_%/-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

arch_patch/%: ## apply hardware architecture specific patches to the Dockerfile
	if [ -e ./$(notdir $@)/Dockerfile.$(ARCH).patch ]; then \
		if [ -e ./$(notdir $@)/Dockerfile.orig ]; then \
               		cp -f ./$(notdir $@)/Dockerfile.orig ./$(notdir $@)/Dockerfile;\
		else\
                	cp -f ./$(notdir $@)/Dockerfile ./$(notdir $@)/Dockerfile.orig;\
		fi;\
		patch -f ./$(notdir $@)/Dockerfile ./$(notdir $@)/Dockerfile.$(ARCH).patch; \
	fi

build/%: DARGS?=
build/%: ## build the latest image for a stack
	docker build $(DARGS) --rm --force-rm -t $(OWNER)/$(notdir $@):latest ./$(notdir $@)

build-all: $(foreach I,$(ALL_IMAGES),arch_patch/$(I) build/$(I) ) ## build all stacks
build-test-all: $(foreach I,$(ALL_IMAGES),arch_patch/$(I) build/$(I) test/$(I) ) ## build and test all stacks

cached-layers/%:
	mkdir -p $(CACHE_DIR)
	docker save $$(docker history -q $(OWNER)/$(notdir $@):latest | grep -v '<missing>') | gzip > $(CACHE_DIR)/$(notdir $@).tar.gz

cached-layers: $(ALL_IMAGES:%=cache/%) ## cache all stacks in tarballs

dev/%: ARGS?=
dev/%: DARGS?=
dev/%: PORT?=8888
dev/%: ## run a foreground container for a stack
	docker run -it --rm -p $(PORT):8888 $(DARGS) $(OWNER)/$(notdir $@) $(ARGS)

layers-from-cache/%:
	-gunzip -c $(CACHE_DIR)/$(notdir $@).tar.gz | docker load

layers-from-cache: $(ALL_IMAGES:%=cache/%) ## load all layers from cached tarballs

push/%: ## push the latest and HEAD git SHA tags for a stack to Docker Hub
	docker push $(OWNER)/$(notdir $@):latest
	docker push $(OWNER)/$(notdir $@):$(GIT_MASTER_HEAD_SHA)

push-all: $(ALL_IMAGES:%=push/%) ## push all stacks

retry/%:
	@for i in $$(seq 1 $(RETRIES)); do \
		make $(notdir $@) ; \
		if [[ $$? == 0 ]]; then exit 0; fi; \
		echo "Sleeping for $$((i * 60))s before retry" ; \
		sleep $$((i * 60)) ; \
	done ; exit 1

tag/%: ##tag the latest stack image with the HEAD git SHA
	docker tag -f $(OWNER)/$(notdir $@):latest $(OWNER)/$(notdir $@):$(GIT_MASTER_HEAD_SHA)

tag-all: $(ALL_IMAGES:%=tag/%) ## tag all stacks

test/%: ## run a stack container, check for jupyter server liveliness
	@-docker rm -f iut
	@docker run -d --name iut $(OWNER)/$(notdir $@)
	@for i in $$(seq 0 9); do \
		sleep $$i; \
		docker exec iut bash -c 'wget http://localhost:8888 -O- | grep -i jupyter'; \
		if [[ $$? == 0 ]]; then exit 0; fi; \
	done ; exit 1

test-all: $(ALL_IMAGES:%=test/%) ## test all stacks
