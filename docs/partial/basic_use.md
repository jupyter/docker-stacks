## Basic Use

The following command starts a container with the Notebook server listening for HTTP connections on port 8888 without authentication configured.

```bash
docker run -d -p 8888:8888 jupyter/{{stack_name}}
```
