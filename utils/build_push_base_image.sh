#! /bin/bash

docker build --no-cache -f utils/Dockerfile.base -t asyoez/python3-nltk:latest .
docker push asyoez/python3-nltk:latest  