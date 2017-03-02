#!/bin/sh

docker build -t wg/centos:7  -f Dockerfile-7 .
docker build -t wg/centos    -f Dockerfile-latest .