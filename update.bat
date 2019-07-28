@echo off
echo Updating quadrant data from osm
set WORK_FOLDER=d:\_VFR_LANDMARKS_3D_RU\work_folder
SET QUADRANT=+56+038
set WORK_FOLDER=%WORK_FOLDER%\%QUADRANT%\osm_data

echo Quadrant: %QUADRANT%
echo Working folder: %WORK_FOLDER%

IF EXIST "%WORK_FOLDER%\+56+038_new.pbf" (
  del "%WORK_FOLDER%\+56+038.pbf"
  ren "%WORK_FOLDER%\+56+038_new.pbf" "+56+038.pbf"
) ELSE (
  echo +56+038_new.pbf is missing
)

osmupd "%WORK_FOLDER%\+56+038.pbf" "%WORK_FOLDER%\+56+038_new.pbf" -b=38,56,39,57 -v --keep-tempfiles
osmconvert "%WORK_FOLDER%\+56+038_new.pbf" -o="%WORK_FOLDER%\+56+038.o5m"
pause



