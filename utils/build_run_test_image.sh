#! /bin/bash

docker build -f Dockerfile -t legaldoc:latest . && docker run -ti legaldoc:latest