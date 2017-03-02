#!/bin/sh

(cd ..; docker build -t wg/console -f console/Dockerfile .)