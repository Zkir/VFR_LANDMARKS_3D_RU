@echo off
echo Updating quadrant data from osm

SET QUADRANT=%1
SET BBOX=poly\%~2
set WORK_FOLDER=work_folder\10_osm_extracts\%QUADRANT%
set PLANET= work_folder\00_planet.osm\russia-latest.osm.pbf

echo Quadrant: %QUADRANT%
echo BBOX: %BBOX%
echo Working folder: %WORK_FOLDER%

IF EXIST "%WORK_FOLDER%\%QUADRANT%_new.pbf" (
  del "%WORK_FOLDER%\%QUADRANT%.pbf"
  
) ELSE (
  echo %QUADRANT%_new.pbf is missing
  md "%WORK_FOLDER%"
  osmconvert %PLANET% -B=%BBOX% -o="%WORK_FOLDER%\%QUADRANT%_new.pbf"
)

ren "%WORK_FOLDER%\%QUADRANT%_new.pbf" "%QUADRANT%.pbf"
osmupd "%WORK_FOLDER%\%QUADRANT%.pbf" "%WORK_FOLDER%\%QUADRANT%_new.pbf" -B=%BBOX% -v --keep-tempfiles
osmconvert "%WORK_FOLDER%\%QUADRANT%_new.pbf" -o="%WORK_FOLDER%\%QUADRANT%.o5m"

:end



