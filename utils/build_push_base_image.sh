#! /bin/bash

docker build -f utils/DockerBaseImage -t asyoez/python3-nltk:latest .
docker push asyoez/python3-nltk:latest  