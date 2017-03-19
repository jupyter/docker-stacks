FROM alpine:3.5

# We install py-zmq from alpine, since installing it from pip requires we have
# gcc and build tools installed. manylinux1 wheels don't work on / for alpine yet
RUN apk add --no-cache python3 py-zmq

RUN pip3 install --no-cache-dir notebook ipykernel jupyterhub

CMD ["/usr/bin/jupyter", "notebook", "--ip=0.0.0.0", "--port=8888"]

EXPOSE 8888
