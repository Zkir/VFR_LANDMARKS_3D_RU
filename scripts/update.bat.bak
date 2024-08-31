@echo off
echo Updating quadrant data from osm

SET QUADRANT=%1
SET BBOX=poly\%~2
set WORK_FOLDER=work_folder\10_osm_extracts\%QUADRANT%
set PLANET= work_folder\00_planet.osm\russia-latest.osm.pbf

echo Quadrant: %QUADRANT%
echo BBOX: %BBOX%
echo Working folder: %WORK_FOLDER%

mkdir %WORK_FOLDER%

osmconvert %PLANET% -B=%BBOX% -o="%WORK_FOLDER%\%QUADRANT%_new.pbf"
osmconvert "%WORK_FOLDER%\%QUADRANT%_new.pbf" -o="%WORK_FOLDER%\%QUADRANT%.o5m"

:end



