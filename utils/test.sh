#! /bin/bash

docker build --no-cache -f ./utils/Dockerfile.test -t legaldoc:latest . && docker run -ti legaldoc:latest