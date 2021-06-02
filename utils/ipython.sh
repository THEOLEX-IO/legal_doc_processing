#! /bin/bash

docker build --no-cache -f ./utils/Dockerfile.ipython -t legaldoc:latest . && docker run -ti legaldoc:latest