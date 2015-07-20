.PHONY: build dev help 

OWNER:=jupyter
STACK?=

help:
	@echo
	@echo 'build STACK=<dirname> - build using Dockerfile in named directory'
	@echo '  dev STACK=<dirname> - run container using stack name'
	@echo

build:
	@cd $(STACK) && \
		docker build --rm --force-rm -t $(OWNER)/$(STACK) .

dev:
	docker run -it --rm -p 8888:8888 $(OWNER)/$(STACK)