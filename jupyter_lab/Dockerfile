From python:3.6.1-alpine

RUN apk update \
    && apk add build-base \
    && pip install jupyter \
    && pip install jupyterlab \
    && pip install ecdsa 

EXPOSE 8888

WORKDIR /work

CMD [ "jupyter", "notebook", "--no-browser" , "--ip=0.0.0.0" , "--allow-root"]

#to build just run 
#docker build -t python36_jupyter .