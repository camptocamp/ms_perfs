#!/bin/bash

sed -e 's/host=db port=5432/host=localhost port=15432/' < qgis/project.qgs > qgis/project_ext.qgs
