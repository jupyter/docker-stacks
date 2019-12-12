#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

SPARKMAGIC_CONFIG_CREDENTIALS_AUTH=${SPARKMAGIC_CONFIG_CREDENTIALS_AUTH:-None}
SPARKMAGIC_CONFIG_CREDENTIALS_USERNAME=${SPARKMAGIC_CONFIG_CREDENTIALS_USERNAME:-}
SPARKMAGIC_CONFIG_CREDENTIALS_PASSWORD=${SPARKMAGIC_CONFIG_CREDENTIALS_PASSWORD:-}
SPARKMAGIC_CONFIG_CREDENTIALS_URL=${SPARKMAGIC_CONFIG_CREDENTIALS_URL:-http://spark-livy:8998}

SPARKMAGIC_CONFIG_LOG_LEVEL=${SPARKMAGIC_CONFIG_LOG_LEVEL:-DEBUG}
SPARKMAGIC_CONFIG_MAX_RESULTS_SQL=${SPARKMAGIC_CONFIG_MAX_RESULTS_SQL:-2500}
SPARKMAGIC_CONFIG_LIVY_SERVER_HEARTBEAT=${SPARKMAGIC_CONFIG_LIVY_SERVER_HEARTBEAT:-0}
SPARKMAGIC_CONFIG_LIVY_SESSION_STARTUP_TIMEOUT=${SPARKMAGIC_CONFIG_LIVY_SESSION_STARTUP_TIMEOUT:-60}
SPARKMAGIC_CONFIG_SESSION_CONFIG=${SPARKMAGIC_CONFIG_SESSION_CONFIG:-"{}"}

if [ -z "$SPARKMAGIC_CONFIG" ]; then

SPARKMAGIC_CONFIG=$(cat <<-END
{
    "kernel_python_credentials": {
        "username": "$SPARKMAGIC_CONFIG_CREDENTIALS_USERNAME",
        "password": "$SPARKMAGIC_CONFIG_CREDENTIALS_PASSWORD",
        "url": "$SPARKMAGIC_CONFIG_CREDENTIALS_URL",
        "auth": "$SPARKMAGIC_CONFIG_CREDENTIALS_AUTH"
    },
    "kernel_scala_credentials": {
        "username": "$SPARKMAGIC_CONFIG_CREDENTIALS_USERNAME",
        "password": "$SPARKMAGIC_CONFIG_CREDENTIALS_PASSWORD",
        "url": "$SPARKMAGIC_CONFIG_CREDENTIALS_URL",
        "auth": "$SPARKMAGIC_CONFIG_CREDENTIALS_AUTH"
    },
    "kernel_r_credentials": {
        "username": "$SPARKMAGIC_CONFIG_CREDENTIALS_USERNAME",
        "password": "$SPARKMAGIC_CONFIG_CREDENTIALS_PASSWORD",
        "url": "$SPARKMAGIC_CONFIG_CREDENTIALS_URL",
        "auth": "$SPARKMAGIC_CONFIG_CREDENTIALS_AUTH"
    },
    "logging_config": {
        "version": 1,
        "formatters": {
            "magicsFormatter": {
                "format": "%(asctime)s\t%(levelname)s\t%(message)s",
                "datefmt": ""
            }
        },
        "handlers": {
            "magicsHandler": {
                "class": "logging.FileHandler",
                "formatter": "magicsFormatter",
                "filename": "/dev/stdout",
                "mode": "w"
            }
        },
        "loggers": {
            "magicsLogger": {
                "handlers": [
                    "magicsHandler"
                ],
                "level": "DEBUG",
                "propagate": 0
            }
        }
    },
    "wait_for_idle_timeout_seconds": 15,
    "livy_session_startup_timeout_seconds": $SPARKMAGIC_CONFIG_LIVY_SESSION_STARTUP_TIMEOUT,
    "fatal_error_suggestion": "The code failed because of a fatal error:\n\t{}.\n\nSome things to try:\na) Make sure Spark has enough available resources for Jupyter to create a Spark context.\nb) Contact your Jupyter administrator to make sure the Spark magics library is configured correctly.\nc) Restart the kernel.",
    "ignore_ssl_errors": false,
    "session_configs": $SPARKMAGIC_CONFIG_SESSION_CONFIG,
    "use_auto_viz": true,
    "coerce_dataframe": true,
    "max_results_sql": $SPARKMAGIC_CONFIG_MAX_RESULTS_SQL,
    "pyspark_dataframe_encoding": "utf-8",
    "heartbeat_refresh_seconds": 30,
    "livy_server_heartbeat_timeout_seconds": $SPARKMAGIC_CONFIG_LIVY_SERVER_HEARTBEAT,
    "heartbeat_retry_seconds": 10,
    "server_extension_default_kernel_name": "pysparkkernel",
    "custom_headers": {},
    "retry_policy": "configurable",
    "retry_seconds_to_sleep_list": [0.2, 0.5, 1, 3, 5],
    "configurable_retry_policy_max_retries": 8
}
END
)

fi

printf "%s" "$SPARKMAGIC_CONFIG" > /home/$NB_USER/.sparkmagic/config.json
chown $NB_USER:$NB_GID /home/$NB_USER/.sparkmagic/config.json
