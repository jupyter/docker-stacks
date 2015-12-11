# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

letsencrypt: NAME?=notebook
letsencrypt: SECRETS_VOLUME?=$(NAME)-secrets
letsencrypt:
	@test -n "$(FQDN)" || \
		(echo "ERROR: FQDN not defined or blank"; exit 1)
	@test -n "$(EMAIL)" || \
		(echo "ERROR: EMAIL not defined or blank"; exit 1)
	@docker volume create --name $(SECRETS_VOLUME) > /dev/null
	-@docker rm letsencrypt 2> /dev/null
	@docker run -it -p 80:80 --name letsencrypt \
		-v $(SECRETS_VOLUME):/secrets \
		quay.io/letsencrypt/letsencrypt:latest \
		certonly \
		--standalone \
		--standalone-supported-challenges http-01 \
		--cert-path /secrets/cert.pem \
		--key-path /secrets/privkey.pem \
		--chain-path /secrets/chain.pem \
		--fullchain-path /secrets/fullchain.pem \
		--agree-tos \
		--duplicate \
		--domain '$(FQDN)' \
		--email '$(EMAIL)'
	@docker rm letsencrypt > /dev/null

letsencrypt-notebook: PORT?=443
letsencrypt-notebook: NAME?=notebook
letsencrypt-notebook: WORK_VOLUME?=$(NAME)-data
letsencrypt-notebook: SECRETS_VOLUME?=$(NAME)-secrets
letsencrypt-notebook: DOCKER_ARGS:=-e USE_HTTPS=yes \
	-e PASSWORD=$(PASSWORD) \
	-v $(SECRETS_VOLUME):/secrets
letsencrypt-notebook: PRE_CMD:=chown -R jovyan /secrets; \
 	chmod 600 /secrets/*;
letsencrypt-notebook: ARGS:=\
	--NotebookApp.certfile=/secrets/fullchain.pem \
	--NotebookApp.keyfile=/secrets/privkey.pem
letsencrypt-notebook: check
	@test -n "$(PASSWORD)" || \
		(echo "ERROR: PASSWORD not defined or blank"; exit 1)
	$(RUN_NOTEBOOK)
