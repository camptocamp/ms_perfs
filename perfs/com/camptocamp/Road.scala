package com.camptocamp

import io.gatling.core.Predef._
import io.gatling.core.scenario.Simulation
import io.gatling.http.Predef._

import scala.concurrent.duration._

class Road extends Simulation {
  val httpConf = http
    .baseURL("http://localhost/qgis")
    .acceptHeader("image/png")
    .acceptEncodingHeader("gzip, deflate")

  val fetchTile = exec(
    http("${level}").
      //get("?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=${minY},${minX},${maxY},${maxX}&LAYERS=roads_dashed" + PerfConfig.commonParams))
      get("?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=${minY},${minX},${maxY},${maxX}&LAYERS=roads_simple" + PerfConfig.commonParams))

  val steps: Seq[Int] = 0 to PerfConfig.nbSteps
  val scn = scenario("User").foreach(steps.reverse, "level") {
    during(20 seconds, "tries", false) {
      exec(session => PerfConfig.addRandomTileInfo(session)).exec(fetchTile)
    }
  }

  setUp(
    scn.inject(atOnceUsers(1))
  ).protocols(httpConf)
}
