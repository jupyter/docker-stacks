# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

self-signed-notebook: PORT?=443
self-signed-notebook: NAME?=notebook
self-signed-notebook: WORK_VOLUME?=$(NAME)-data
self-signed-notebook: DOCKER_ARGS:=-e USE_HTTPS=yes \
	-e PASSWORD=$(PASSWORD)
self-signed-notebook: check
	@test -n "$(PASSWORD)" || \
		(echo "ERROR: PASSWORD not defined or blank"; exit 1)
	$(RUN_NOTEBOOK)
