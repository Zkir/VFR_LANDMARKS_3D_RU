@echo off
SET WORK_FOLDER=%1
pushd %WORK_FOLDER%
echo download source osm file

rem SET REGION=europe/
rem SET COUNTRY=united-kingdom
SET REGION=
SET COUNTRY=planet

if "%COUNTRY%"=="planet" goto planet

:country
aria2c https://download.geofabrik.de/%REGION%%COUNTRY%-latest.osm.pbf

goto end 
:planet
rem rm -f planet-*.osm.pbf 
del /Q /F planet-*.osm.pbf 
aria2c https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf.torrent --seed-time=0  --out=planet-latest.osm.pbf.torrent
ren planet-*.osm.pbf planet-latest.osm.pbf

:end
popd