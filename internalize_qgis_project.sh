#!/bin/bash

sed -e 's/host=localhost port=15432/host=db port=5432/' < qgis/project_ext.qgs > qgis/project.qgs
