package com.camptocamp

import io.gatling.core.session.{Expression, Session}

import scala.util.Random

object PerfConfig {
  def getConf(name: String, default: Int): Int = {
    val result = System.getenv(name)
    if (result != null) return result.toInt
    default
  }

  def getConf[T](name: String, default: String): String = {
    val result = System.getenv(name)
    if (result != null) return result
    default
  }

  val stepFactor = 1.2
  val nbSteps = 7
  val ratio = 4.0 / 3.0
  val minX = 7
  val minY = 46
  val maxX = 9.5
  val maxY = 47.5
  val defaultBaseUrls = "http://localhost:8081/|MapServer,http://localhost:8083/|QGIS,http://localhost:8082/OSM/ows|GeoServer"
  val baseUrlMap: Map[String, String] = getConf("base_urls", defaultBaseUrls).split(",").map(a => {
    val s = a.split("\\|")
    (s(0), s(1))
  }).toMap
  val baseUrls: Seq[String] = baseUrlMap.keys.toSeq
  val layers = getConf("layers", "amenities_class,roads_dashed,building_hatched,amenities_simple,roads_simple,building_simple").split(",")
  val nbUsers: Int = getConf("nb_users", 1)

  val maxWidth = maxX - minX
  val maxHeight = maxY - minY
  val pixelWidth = 800
  val pixelHeight = (pixelWidth / ratio).toInt
  val commonParams: Any = s"&CRS=EPSG:4326&WIDTH=${pixelWidth}&HEIGHT=${pixelHeight}&" +
    s"STYLES=&FORMAT=image/png&DPI=96&MAP_RESOLUTION=96&" +
    "FORMAT_OPTIONS=dpi:96&TRANSPARENT=TRUE"


  val random = new Random

  def randomTileInfo(level: Int) = {
    val width = maxWidth / Math.pow(stepFactor, level)
    val height = width / ratio
    val x = minX + (random.nextDouble() * (maxWidth - width))
    val y = minY + (random.nextDouble() * (maxHeight - height))
    val layer = layers(random.nextInt(layers.length))
    Map("minX" -> x, "minY" -> y, "maxX" -> (x + width), "maxY" -> (y + height), "level" -> level, "layer" -> layer)
  }

  def addRandomTileInfo(session: Session): Session = {
    session.setAll(randomTileInfo(session("level").as[Int]))
  }
}
