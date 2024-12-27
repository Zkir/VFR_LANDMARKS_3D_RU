@echo off
SET WORK_FOLDER=%1
cd %WORK_FOLDER%
echo download source osm file

rem SET REGION=europe/
rem SET COUNTRY=united-kingdom
SET REGION=
SET COUNTRY=planet

if %COUNTRY%=="planet" goto planet

:country
aria2c https://download.geofabrik.de/%REGION%%COUNTRY%-latest.osm.pbf

goto end 
:planet
rm -f data/planet-*.osm.pbf 
aria2c https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf.torrent --seed-time=0
mv data/planet-*.osm.pbf planet-latest.osm.pbf

:end