#!/bin/bash

if [[ "$(docker images -q flaskweb:$1 2> /dev/null)" != "" ]]; then
	docker rmi -f flaskweb:$1
fi

docker build -t flaskweb:$1 .

if [[ "$(docker inspect flaskweb 2> /dev/null | grep '"Name": "/flaskweb"')" != "" ]]; then
	docker rm -f flaskweb
fi

docker run -d --restart=always -p 8085:8085 --name flaskweb flaskweb:$1