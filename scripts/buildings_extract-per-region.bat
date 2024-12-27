@echo off
SET QUADRANT=%1
SET BBOX=poly\%~2
set WORK_FOLDER=work_folder\10_osm_extracts\%QUADRANT%
set PLANET=work_folder\05_global_extracts
IF NOT EXIST %WORK_FOLDER% mkdir %WORK_FOLDER%
osmconvert %PLANET%\objects-all.osm  -B=%BBOX% -o="%WORK_FOLDER%\objects-all.osm"
osmconvert %PLANET%\objects-with-parts.osm  -B=%BBOX% -o="%WORK_FOLDER%\objects-with-parts.osm" 
osmconvert %PLANET%\geocoder.osm  -B=%BBOX% -o="%WORK_FOLDER%\geocoder.osm" 
:end