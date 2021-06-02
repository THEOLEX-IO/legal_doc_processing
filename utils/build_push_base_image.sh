#! /bin/bash

docker build --no-cache -f utils/DockerBaseImage -t asyoez/python3-nltk:latest .
docker push asyoez/python3-nltk:latest  