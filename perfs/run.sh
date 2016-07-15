#!/bin/sh

until wget "http://mapserver/?SERVICE=WMS&REQUEST=GetCapabilities" -O /dev/null
do
    echo "Waiting for mapserver"
    sleep 1
done

until wget "http://geoserver:8080/?SERVICE=WMS&REQUEST=GetCapabilities" -O /dev/null
do
    echo "Waiting for geoserver"
    sleep 1
done

until wget "http://qgis/?SERVICE=WMS&REQUEST=GetCapabilities" -O /dev/null
do
    echo "Waiting for QGIS"
    sleep 1
done

export base_urls="http://geoserver:8080/OSM/ows|GeoServer,http://mapserver/|MapServer,http://qgis/|QGIS"

rm -r $GATLING_HOME/results/*

for nb_users in 1 2 5 10 20 40
do
    export nb_users=$nb_users
    gatling.sh -sf $GATLING_HOME/user-files/simulations -s com.camptocamp.Test
done

cd $GATLING_HOME/results/
mkdir all
for dir in test-*
do
    cp ${dir}/simulation.log all/${dir}.log
done

gatling.sh -ro all
