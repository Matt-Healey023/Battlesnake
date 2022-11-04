#!/bin/bash

sudo docker kill battlesnake
sudo docker rm battlesnake

git pull origin main
sudo docker build -t battlesnake .

sudo docker run -d -p 8001:8001 --name battlesnake battlesnake

sudo docker rmi $(sudo docker images -f "dangling=true" -q)
