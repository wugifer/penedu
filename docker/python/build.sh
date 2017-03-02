#!/bin/sh

(cd ..; docker build -t wg/python -f python/Dockerfile .)