#!/bin/bash
set -e 
set -x

docker build -t confusion2 . 
docker run -itd --name confusion2 -p 23334:23333 -u ctf confusion2


