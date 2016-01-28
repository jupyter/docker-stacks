# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

.PHONY: build help release

REPO:=jupyter/ubuntu_14_04_locale_fix:latest

help:
	@echo 'make build release'
	@echo 'See https://github.com/jupyter/docker-stacks/pull/108'

build: DARGS?=
build:
	docker build $(DARGS) --rm --force-rm -t $(REPO):latest .

release:
	docker push $(REPO):latest
