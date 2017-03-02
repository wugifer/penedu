#!/bin/sh

# project root dir, absolute path
root_dir=$(cd $(dirname "$0"); cd ..; pwd)
echo $root_dir

# internal docker: es, mysql, redis

#links="--link es --link mysql --link redis -v /opt/project:/opt/project"
links="-v /src/penedu:/src/penedu"

# outter docker: nginx and console(for inner dokcer debug)
# -p 5091:5081 is for debug: in console docker, start 5081, out docker, can visit 5091
docker run -d       --name nginx   -p 5000:5000 $links              -e PYTHONIOENCODING=utf-8 wg/python
docker run --rm -it --name console              $links --link nginx -e PYTHONIOENCODING=utf-8 wg/console

# stop and remove containers
docker stop nginx console
docker rm   nginx console

