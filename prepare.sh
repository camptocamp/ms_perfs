#!/bin/bash
set -e

if [[ ! -d docker-osm ]]
then
    git clone git@github.com:pvalsecc/docker-osm.git
else
    (cd docker-osm; git pull --rebase) || true
fi

if [[ ! -d OSM-Shapefile-QGIS-stylesheets ]]
then
    git clone git@github.com:charleyglynn/OSM-Shapefile-QGIS-stylesheets.git
fi

if [[ ! -d QGIS-resources ]]
then
    git clone git@github.com:anitagraser/QGIS-resources.git
fi

cd docker-osm

if [[ ! -f settings/country.pbf ]]
then
    python pbf_downloader.py switzerland
fi

docker-compose build
docker-compose up
