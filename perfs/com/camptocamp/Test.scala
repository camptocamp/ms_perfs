package com.camptocamp

import io.gatling.core.Predef._
import io.gatling.core.scenario.Simulation
import io.gatling.http.Predef._

import scala.concurrent.duration._

class Test extends Simulation {


  val httpConf = http
    .acceptHeader("image/png")
    .acceptEncodingHeader("gzip, deflate")

  val fetchTile = group("${layer}") {
    exec(
      http("${level}").
        get("${base_url}?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=${minY},${minX},${maxY},${maxX}&LAYERS=${layer}" + PerfConfig.commonParams))
  }



  val steps: Seq[Int] = (0 to PerfConfig.nbSteps)
  val scn = scenario("User").group(_ => PerfConfig.nbUsers.toString) {
    foreach(PerfConfig.baseUrls, "base_url") {
      group(session => PerfConfig.baseUrlMap(session("base_url").as[String])) {
        foreach(steps.reverse, "level") {
          exec(session => {
            println("Starting level " + session("level").as[String])
            session
          })
            .during(30 seconds) {
              exec(session => PerfConfig.addRandomTileInfo(session)).exec(fetchTile)
            }
            .exec(session => {
              println("Done level " + session("level").as[String])
              session
            })
        }
      }
    }
  }

  setUp(
    scn.inject(rampUsers(PerfConfig.nbUsers) over (1 seconds))
  ).protocols(httpConf)
}
