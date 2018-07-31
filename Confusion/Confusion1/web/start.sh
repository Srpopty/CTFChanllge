#!/bin/bash
set -e 
set -x

docker build -t confusion1 . 
docker run -itd --name confusion1 -p 23333:23333 -u ctf confusion1


