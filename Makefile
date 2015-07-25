.PHONY: build dev help server

OWNER:=jupyter
STACK?=
ARGS?=
DARGS?=

help:
	@echo
	@echo ' build STACK=<dirname> - build using Dockerfile in named directory'
	@echo '   dev STACK=<dirname> - run container using stack name'
	@echo 'server STACK=<dirname> - run stack container in background'
	@echo

build:
	@cd $(STACK) && \
		docker build --rm --force-rm -t $(OWNER)/$(STACK) .

dev:
	@docker run -it --rm -p 8888:8888 $(DARGS) $(OWNER)/$(STACK) $(ARGS)

server:
	@docker run -d -p 8888:8888 $(DARGS) $(OWNER)/$(STACK) $(ARGS)