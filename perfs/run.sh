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

until wget "http://geoserver-jai:8080/?SERVICE=WMS&REQUEST=GetCapabilities" -O /dev/null
do
    echo "Waiting for geoserver-jai"
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

export base_urls="${BASE_URLS:-http://geoserver:8080/OSM/ows|GeoServer,http://geoserver-jai:8080/OSM/ows|GeoServer-jai,http://mapserver/|MapServer,http://qgis2/|QGIS2,http://qgis3/|QGIS3}"
echo "base_urls=$base_urls"

warmup=${WARMUP:-1}

if [ $warmup == '1' ]
then
    echo "warmup round (results are trashed)"
    export nb_users=1
    export time=30
    gatling.sh -sf $GATLING_HOME/user-files/simulations -s com.camptocamp.Test

fi
rm -r $GATLING_HOME/results/*

export time=${TIME_PER_TEST:-120}  # time to keep measing for a given server and a given zoom level
users=${USERS:-1 2 5 10 20 40}
for nb_users in $users
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
