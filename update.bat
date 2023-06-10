@echo off
echo Updating quadrant data from osm
set WORK_FOLDER=d:\_VFR_LANDMARKS_3D_RU\work_folder
rem SET QUADRANT=+56+038
rem SET BBOX=38,56,39,57
SET QUADRANT=%1
SET BBOX=poly\%~2
set WORK_FOLDER=%WORK_FOLDER%\%QUADRANT%\osm_data
set PLANET= d:\_planet.osm\russia-latest.osm.pbf

echo Quadrant: %QUADRANT%
echo BBOX: %BBOX%
echo Working folder: %WORK_FOLDER%

IF EXIST "%WORK_FOLDER%\%QUADRANT%_new.pbf" (
  del "%WORK_FOLDER%\%QUADRANT%.pbf"
  
) ELSE (
  echo %QUADRANT%_new.pbf is missing
  md "%WORK_FOLDER%"
  md "%WORK_FOLDER%/../osm_3dmodels"
  osmconvert %PLANET% -B=%BBOX% -o="%WORK_FOLDER%\%QUADRANT%_new.pbf"
)

ren "%WORK_FOLDER%\%QUADRANT%_new.pbf" "%QUADRANT%.pbf"
osmupd "%WORK_FOLDER%\%QUADRANT%.pbf" "%WORK_FOLDER%\%QUADRANT%_new.pbf" -B=%BBOX% -v --keep-tempfiles
osmconvert "%WORK_FOLDER%\%QUADRANT%_new.pbf" -o="%WORK_FOLDER%\%QUADRANT%.o5m"

:end



