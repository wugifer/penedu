#!/bin/sh

(echo; echo centos;  cd centos;  sh build.sh)
(echo; echo python;  cd python;  sh build.sh)
(echo; echo console;  cd console;  sh build.sh)
