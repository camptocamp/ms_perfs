#!/bin/bash
set -e

if [[ ! -d docker-osm ]]
then
    git clone git@github.com:pvalsecc/docker-osm.git
else
    (cd docker-osm; git pull --rebase) || true
fi

cd docker-osm

if [[ ! -f settings/country.pbf ]]
then
    python pbf_downloader.py switzerland
fi

docker-compose build
docker-compose up
