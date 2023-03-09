#!/bin/bash

set -e

tag=$1

if [[ -z "$tag" ]];then
    echo "Must supply tag"
    exit 1
fi

repo="registry.apps.kvecchione.com"
image="savingstracker"

docker build -t $repo/$image:$tag .
docker tag $repo/$image:$tag $repo/$image:latest
docker push $repo/$image:$tag
docker push $repo/$image:latest