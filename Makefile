# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

.PHONY: build-all help environment-check release-all

OWNER:=jupyter
# need to list these manually because there's a dependency tree
ALL_STACKS:=base-notebook \
	minimal-notebook \
	r-notebook \
	scipy-notebook \
	datascience-notebook \
	pyspark-notebook \
	all-spark-notebook

ALL_IMAGES:=$(ALL_STACKS)

GIT_MASTER_HEAD_SHA:=$(shell git rev-parse --short=12 --verify HEAD)

help:
	@echo
	@echo '   build/<stack dirname> - builds the latest image for the stack'
	@echo '     dev/<stack dirname> - runs a foreground container for the stack'
	@echo '    push/<stack dirname> - pushes the latest and HEAD git SHA tags for the stack to Docker Hub'
	@echo ' refresh/<stack dirname> - runs a foreground container for the stack'
	@echo '             release-all - refresh, build, tag, and push all stacks'
	@echo '     tag/<stack-dirname> - tags the latest stack image with the HEAD git SHA'

build/%: DARGS?=

build/%:
	docker build $(DARGS) --rm --force-rm -t $(OWNER)/$(notdir $@):latest ./$(notdir $@)

build-all: $(patsubst %,build/%, $(ALL_IMAGES))

dev/%: ARGS?=
dev/%: DARGS?=
dev/%: PORT?=8888
dev/%:
	docker run -it --rm -p $(PORT):8888 $(DARGS) $(OWNER)/$(notdir $@) $(ARGS)

environment-check:
	test -e ~/.docker-stacks-builder

push/%:
	docker push $(OWNER)/$(notdir $@):latest
	docker push $(OWNER)/$(notdir $@):$(GIT_MASTER_HEAD_SHA)

push-all: $(patsubst %,push/%, $(ALL_IMAGES))

refresh/%:
# skip if error: a stack might not be on dockerhub yet
	-docker pull $(OWNER)/$(notdir $@):latest

refresh-all: $(patsubst %,refresh/%, $(ALL_IMAGES))

release-all: environment-check refresh-all build-all tag-all push-all

tag/%:
# always tag the latest build with the git sha
	docker tag -f $(OWNER)/$(notdir $@):latest $(OWNER)/$(notdir $@):$(GIT_MASTER_HEAD_SHA)

tag-all: $(patsubst %,tag/%, $(ALL_IMAGES))
