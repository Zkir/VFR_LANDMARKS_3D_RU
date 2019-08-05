@echo off
echo Updating quadrant data from osm
set WORK_FOLDER=d:\_VFR_LANDMARKS_3D_RU\work_folder
rem SET QUADRANT=+56+038
rem SET BBOX=38,56,39,57
SET QUADRANT=%1
SET BBOX=%~2
set WORK_FOLDER=%WORK_FOLDER%\%QUADRANT%\osm_data

echo Quadrant: %QUADRANT%
echo BBOX: %BBOX%
echo Working folder: %WORK_FOLDER%

IF EXIST "%WORK_FOLDER%\%QUADRANT%_new.pbf" (
  del "%WORK_FOLDER%\%QUADRANT%.pbf"
  ren "%WORK_FOLDER%\%QUADRANT%_new.pbf" "%QUADRANT%.pbf"
) ELSE (
  echo %QUADRANT%_new.pbf is missing
  md "%WORK_FOLDER%"
  goto end
)

osmupd "%WORK_FOLDER%\%QUADRANT%.pbf" "%WORK_FOLDER%\%QUADRANT%_new.pbf" -b=%BBOX% -v --keep-tempfiles
osmconvert "%WORK_FOLDER%\%QUADRANT%_new.pbf" -o="%WORK_FOLDER%\%QUADRANT%.o5m"

:end



