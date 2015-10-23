# Copyright (c) Jupyter Development Team.

.PHONY: build dev help server

OWNER:=jupyter
# need to list these manually because there's a dependency tree
ALL_STACKS:=minimal-notebook \
	r-notebook \
	scipy-notebook \
	datascience-notebook \
	pyspark-notebook \
	all-spark-notebook
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

refresh/%:
	docker pull $(OWNER)/$(notdir $@):latest

release-all: environment-check \
	$(patsubst %,refresh/%, $(ALL_STACKS)) \
	$(patsubst %,build/%, $(ALL_STACKS)) \
	$(patsubst %,tag/%, $(ALL_STACKS)) \
	$(patsubst %,push/%, $(ALL_STACKS))

tag/%:
	docker tag $(OWNER)/$(notdir $@):latest $(OWNER)/$(notdir $@):$(GIT_MASTER_HEAD_SHA)
