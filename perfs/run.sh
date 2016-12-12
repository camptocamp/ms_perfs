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

until wget "http://qgis2/?SERVICE=WMS&REQUEST=GetCapabilities" -O /dev/null
do
    echo "Waiting for QGIS2"
    sleep 1
done

until wget "http://qgis3/?SERVICE=WMS&REQUEST=GetCapabilities" -O /dev/null
do
    echo "Waiting for QGIS3"
    sleep 1
done

export base_urls="http://geoserver:8080/OSM/ows|GeoServer,http://mapserver/|MapServer,http://qgis2/|QGIS2,http://qgis3/|QGIS3"

echo "warmup round (results are trashed)"
export nb_users=1
export time=30
gatling.sh -sf $GATLING_HOME/user-files/simulations -s com.camptocamp.Test

rm -r $GATLING_HOME/results/*

export time=120  # time to keep measing for a given server and a given zoom level
for nb_users in 1 2 5 10 20 40
do
    echo "Measuring with $nb_users users in //"
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
