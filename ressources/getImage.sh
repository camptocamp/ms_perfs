#!/bin/bash

# Require bash 4
declare -A SCRIPT={}
declare -A PORT={}
declare -A CRS={}

PORT['MapServer']=8081
PORT['GeoServer']=8082
PORT['QGIS2']=8084
PORT['QGIS3']=8083

SCRIPT['MapServer']=""
SCRIPT['GeoServer']=ows
SCRIPT['QGIS2']=""
SCRIPT['QGIS3']=""

CRS['MapServer']="EPSG:4326"
CRS['GeoServer']="EPSG:4326"
CRS['QGIS2']="EPSG:4326"
CRS['QGIS3']="EPSG:4326"

function saveWMSImages {
  for SERVER in QGIS2 QGIS3 MapServer GeoServer
  do
    mkdir ${SERVER}
    echo $SERVER ${PORT[${SERVER}]}
      echo $LAYER
      #echo "http://localhost:${PORT[${SERVER}]}/${SCRIPT[${SERVER}]}?SERVICE=WMS&REQUEST=GetMap&LAYERS=${LAYER}&CRS=${CRS[${SERVER}]}&VERSION=1.3.0&BBOX=${BBOX}&WIDTH=400&HEIGHT=400&FORMAT=image/png"
      curl -s "http://localhost:${PORT[${SERVER}]}/${SCRIPT[${SERVER}]}?SERVICE=WMS&REQUEST=GetMap&LAYERS=${LAYER}&CRS=${CRS[${SERVER}]}&VERSION=1.3.0&BBOX=${BBOX}&WIDTH=400&HEIGHT=400&FORMAT=image/png" -o ${SERVER}/${LAYER}${SUFFIX}.png
  done
}

SUFFIX="_nonsquare"
LAYER="amenities_simple"
BBOX="46.5210,6.6297,46.5250,6.6359"
saveWMSImages

SUFFIX="_square"
LAYER="amenities_simple"
BBOX="46.5210,6.6308,46.5250,6.6348"
saveWMSImages

LAYER="amenities_class"
BBOX="46.5210,6.6297,46.5250,6.6359"
saveWMSImages

LAYER="roads_simple"
BBOX="46.5223,6.6304,46.5243,6.6336"
saveWMSImages

LAYER=roads_dashed
BBOX="46.5223,6.6304,46.5243,6.6336"
saveWMSImages

LAYER=building_simple
BBOX="46.5262,6.6264,46.5281,6.6295"
saveWMSImages

LAYER=building_hatched
BBOX="46.5262,6.6264,46.5281,6.6295"
saveWMSImages



