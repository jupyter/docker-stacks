[![docker pulls](https://img.shields.io/docker/pulls/jupyter/sparkmagic-notebook.svg)](https://hub.docker.com/r/jupyter/sparkmagic-notebook/) [![docker stars](https://img.shields.io/docker/stars/jupyter/sparkmagic-notebook.svg)](https://hub.docker.com/r/jupyter/sparkmagic-notebook/) [![image metadata](https://images.microbadger.com/badges/image/jupyter/sparkmagic-notebook.svg)](https://microbadger.com/images/jupyter/sparkmagic-notebook "jupyter/sparkmagic-notebook image metadata")

# Sparkmagic Jupyter Notebook Stack

Please visit the documentation site for help using and contributing to this image and others.

* [Jupyter Docker Stacks on ReadTheDocs](http://jupyter-docker-stacks.readthedocs.io/en/latest/index.html)
* [Selecting an Image :: Core Stacks :: jupyter/sparkmagic-notebook](http://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-sparkmagic-notebook)


# Environment variables

### SPARKMAGIC_CONFIG_CREDENTIALS_AUTH
- Description : Authentication method to use when invoking the livy api
- Default value : `None`

See : https://github.com/jupyter-incubator/sparkmagic#authentication-methods

### SPARKMAGIC_CONFIG_CREDENTIALS_URL
- Description : Address where the remote livy api is running
- Default value : `None`

See : https://livy.apache.org

### SPARKMAGIC_CONFIG_CREDENTIALS_USERNAME
- Description : livy api username
- Default value : ``

### SPARKMAGIC_CONFIG_CREDENTIALS_PASSWORD
- Description : livy api password
- Default value : ``

### SPARKMAGIC_CONFIG_LOG_LEVEL
- Description : Sparkmagic log level
- Default value : `DEBUG`

### SPARKMAGIC_CONFIG_MAX_RESULTS_SQL
- Description : Max number of results for a sql query
- Default value : `2500`

### SPARKMAGIC_CONFIG_LIVY_SESSION_STARTUP_TIMEOUT
- Description : Livy session startup timeout
- Default value : `60`

### SPARKMAGIC_CONFIG_SESSION_CONFIG
- Description : Json string containing Map of key=val spark configuration properties
- Default value : `{}`

### SPARKMAGIC_CONFIG
- Description : Json string containing the `config.json` used by sparkmagic, if this property is set all  the other configurations are going to be ignored.
- Default value :
```json
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
```
