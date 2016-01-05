# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

softlayer-vm: export SOFTLAYER_CPU?=4
softlayer-vm: export SOFTLAYER_DISK_SIZE?=100
softlayer-vm: export SOFTLAYER_MEMORY?=4096
softlayer-vm: export SOFTLAYER_REGION?=wdc01
softlayer-vm: check
	@test -n "$(NAME)" || \
		(echo "ERROR: NAME not defined (make help)"; exit 1)
	@test -n "$(SOFTLAYER_API_KEY)" || \
		(echo "ERROR: SOFTLAYER_API_KEY not defined (make help)"; exit 1)
	@test -n "$(SOFTLAYER_USER)" || \
		(echo "ERROR: SOFTLAYER_USER not defined (make help)"; exit 1)
	@test -n "$(SOFTLAYER_DOMAIN)" || \
		(echo "ERROR: SOFTLAYER_DOMAIN not defined (make help)"; exit 1)
	@docker-machine create -d softlayer $(NAME)
	@echo "DONE: Docker host '$(NAME)' up at $$(docker-machine ip $(NAME))"

softlayer-dns: HOST_NAME:=$$(docker-machine active)
softlayer-dns: IP:=$$(docker-machine ip $(HOST_NAME))
softlayer-dns: check
	@which slcli > /dev/null || (echo "softlayer cli not found (pip install softlayer)"; exit 1)
	@test -n "$(SOFTLAYER_DOMAIN)" || \
		(echo "ERROR: SOFTLAYER_DOMAIN not defined (make help)"; exit 1)
	@slcli dns record-add $(SOFTLAYER_DOMAIN) $(HOST_NAME) A $(IP)
