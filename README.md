# Performance comparison for MapServer, QGIS server and GeoServer

## Dependencies

* docker-compose: 1.8.1
* docker: 1.10.2

## Setup

You must first setup a DB by importing OSM data (for Switzerland) in it.
To do that:

```bash
./prepare.sh
```

You must let it run until all the OSM data has been imported. Do a `CTRL+C` before
trying to run the servers. It will fill a
PostgresQL DB in the `docker-osm/db` directory.


## Run the servers

To run all the servers at the same time:

```bash
docker-compose up
```

It will start:

* PostgresQL: `psql -h localhost -p 15432 -U docker gis` with `docker` as password
* MapServer: http://localhost:8081/?SERVICE=WMS&REQUEST=GetCapabilities
* GeoServer: http://localhost:8082/ows?SERVICE=WMS&REQUEST=GetCapabilities
* QGIS server: http://localhost:8083/?SERVICE=WMS&REQUEST=GetCapabilities

You can open the `test.qgs` project with QGIS to browse them.


## Run the perf tests

```bash
./measure.sh
```


## Editing the layers provided

### MapServer

The mapfile is there: `mapserver/mapserver.map`

Just edit it or one of the included files.


### GeoServer

Use the admin interface with user=admin password=geoserver: http://localhost:8082/


### QGIS

The `qgis/project.qgs` file cannot be directly open from your desktop client
because the DB connection parameters would be wrong. For avoiding that problem,
a set of scripts are provided to do the translation into a `qgis/project_ext.qgs`
file

Before editing the qgis/project_ext.qgs file with your desktop client, run
`./externalize_qgis_project.sh`. When done, run `./internalize_qgis_project.sh`.

This would do it, for example:

```bash
./externalize_qgis_project.sh; qgis qgis/project_ext.qgs; ./internalize_qgis_project.sh
```

You can also run QGIS from the same docker image as the QGIS server:

```
docker run --rm --add-host db:172.17.0.2 -ti -e DISPLAY=unix${DISPLAY} -v /tmp/.X11-unix:/tmp/.X11-unix -v ${HOME}:${HOME} camptocamp/qgis-server:3 /usr/local/bin/start-client.sh
```
