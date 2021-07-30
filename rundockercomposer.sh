#!/bin/bash
sudo apt install docker
sudo add-apt-repository universe
sudo apt install docker-compose
docker-compose pull
docker-compose up
