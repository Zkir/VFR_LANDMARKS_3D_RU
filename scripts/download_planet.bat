SET WORK_FOLDER=d:\_planet.osm
cd %WORK_FOLDER%
echo download source osm file

rem aria2c https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf.torrent --seed-time=0
aria2c https://download.geofabrik.de/russia-latest.osm.pbf