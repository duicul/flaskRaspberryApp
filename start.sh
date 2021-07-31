#!/bin/bash
set -e
TZ='Europe/Bucharest'; export TZ
pwd > /home/logs/current_dir.log
ls -l > /home/logs/list_workdir.log

CONTAINER_ALREADY_STARTED="CONTAINER_ALREADY_STARTED_PLACEHOLDER"
if [ ! -e $CONTAINER_ALREADY_STARTED ]; then
    touch $CONTAINER_ALREADY_STARTED
    echo "-- First container startup --"
    cp -r /home/dbinit/*.db /home/db
	cp -r /home/jsoninit/*.json /home/json
else
    echo "-- Not first container startup --"
fi

echo > /home/jsoninit/additional_run.json

cd db;ls -l > /home/logs/list_dbdir.log;cd ..;
cd json;ls -l > /home/logs/list_jsondir.log;cd ..;

python3 monitor.py &
uwsgi flaskRaspPi.ini