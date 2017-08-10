#!/bin/bash -x

TAG=$(git rev-parse HEAD | cut -c -7)
if [ "$BRANCH_NAME" == "master" ]; then
    #creates latest tag
    TAG="latest"
fi
DOCKER_REGISTRY=${DOCKER_REGISTRY:-gcr.io/cloud-armory}
IMAGE_ID=${IMAGE_ID:-${DOCKER_REGISTRY}/spinnaker-aws-policy}
IMAGE_VERSION=${IMAGE_ID}:${TAG}
docker run --rm ${IMAGE_VERSION} /policy-diff.sh
