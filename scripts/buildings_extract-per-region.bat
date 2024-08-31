@echo off

SET QUADRANT=%1
SET BBOX=poly\%~2
set WORK_FOLDER=work_folder\10_osm_extracts\%QUADRANT%
set PLANET=work_folder\07_building_data

echo Updating %QUADRANT% quadrant data from osm

mkdir %WORK_FOLDER%

osmconvert %PLANET%\objects-all.osm  -B=%BBOX% -o="%WORK_FOLDER%\objects-all.osm"
osmconvert %PLANET%\objects-with-parts.osm  -B=%BBOX% -o="%WORK_FOLDER%\objects-with-parts.osm" 


:end