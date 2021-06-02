#! /bin/bash

docker build --no-cache -f ./utils/Dockerfile.test -t asyoez/legal_doc_processing_repo:latest
docker run -ti docker push asyoez/legal_doc_processing_repo:latest
docker push asyoez/legal_doc_processing_repo:latest


