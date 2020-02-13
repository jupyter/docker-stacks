#!/usr/bin/env bash
cd $(cd -P -- "$(dirname -- "$0")" && pwd -P)

# Fetching port
PORT=0
HELP=0
while [[ "$#" -gt 0 ]]; do case $1 in
  -p|--port) PORT="$2"; shift;;
  -h|--help) HELP=1;;
  *) echo "Unknown parameter passed: $1"; exit 1;;
esac; shift; done

# Print help
if [[ $HELP != 0 ]]; then
    echo "Usage: $0 -p [port] # port must be an integer with 4 or more digits."
    exit 21
fi

# Check if port is valid
if [[ $PORT != [0-9][0-9][0-9][0-9]* ]]; then
    echo "The port is not set or invalid."
    echo "Usage: $0 -p [port] # port must be an integer with 4 or more digits."
    exit 22
fi

# Build and run the Dockerfile
docker build -t gpu-jupyter -f src/.Dockerfile .
docker run -d -p "$PORT":8888 gpu-jupyter
