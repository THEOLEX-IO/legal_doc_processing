#! /bin/bash

docker build --no-cache -f Dockerfile -t legaldoc:latest . && docker run -ti legaldoc:latest