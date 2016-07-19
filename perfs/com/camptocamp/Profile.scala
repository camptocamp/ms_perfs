package com.camptocamp

import io.gatling.core.Predef._
import io.gatling.core.scenario.Simulation
import io.gatling.http.Predef._

class Profile extends Simulation {


  val httpConf = http
    .baseURL("http://localhost/qgis-callgrind")
    .acceptHeader("image/png")
    .acceptEncodingHeader("gzip, deflate")

  val fetchTile = exec(
    http("GetMap").
      get("?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=${minY},${minX},${maxY},${maxX}&LAYERS=roads_simple" + PerfConfig.commonParams))


  val scn = scenario("User").exec(session => {
    session.set("level", 6)
  }).repeat(3, "tries") {
    exec(session => PerfConfig.addRandomTileInfo(session)).exec(fetchTile)
  }

  setUp(
    scn.inject(atOnceUsers(1))
  ).protocols(httpConf)
}
