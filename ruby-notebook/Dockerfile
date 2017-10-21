# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM jupyter/minimal-notebook

MAINTAINER Jupyter Project <jupyter@googlegroups.com>

USER root

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
      libtool \
      automake \
      autoconf \
      pkg-config \
      libffi-dev \
      libzmq3-dev \
      libczmq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install czmq based on https://github.com/SciRuby/iruby
# CZTop requires CZMQ >= 4.0.0 and ZMQ >= 4.2.0
RUN git clone https://github.com/zeromq/czmq /root/czmq && \
    cd /root/czmq && \
    ./autogen.sh && \
    ./configure && \
    make && \
    make install && \
    rm -rf /root/czmq

# skip installing gem documentation
RUN mkdir -p /usr/local/etc \
  && { \
    echo 'install: --no-document'; \
    echo 'update: --no-document'; \
  } >> /usr/local/etc/gemrc

ENV RUBY_VERSION 2.4.1

RUN conda config --add channels conda-forge
RUN conda install -y ruby="$RUBY_VERSION"

# install bundler based on docker-library/ruby
ENV BUNDLER_VERSION 1.14.5

RUN gem install bundler --version "$BUNDLER_VERSION"

# install things globally, for great justice
# and don't create ".bundle" in all our apps
ENV GEM_HOME /usr/local/bundle
ENV BUNDLE_PATH="$GEM_HOME" \
  BUNDLE_BIN="$GEM_HOME/bin" \
  BUNDLE_SILENCE_ROOT_WARNING=1 \
  BUNDLE_APP_CONFIG="$GEM_HOME"
ENV PATH $BUNDLE_BIN:$PATH
RUN mkdir -p "$GEM_HOME" "$BUNDLE_BIN" \
  && chmod 777 "$GEM_HOME" "$BUNDLE_BIN"


# install iruby & register to jupyter kernelspec
RUN gem install cztop
RUN gem install iruby
RUN iruby register --force
RUN jupyter kernelspec install .ipython/kernels/ruby

RUN chown -R $NB_USER .local

# Switch back to jovyan to avoid accidental container runs as root
USER $NB_USER
