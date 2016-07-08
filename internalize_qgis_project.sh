#!/bin/bash

sed -e 's/host=localhost port=15432/host=db port=5432/' < qgis/project_ext.qgs | \
    sed -e 's!v=".*/symbols/\(.*\.svg\)"!v="./symbols/\1"!' > qgis/project.qgs
