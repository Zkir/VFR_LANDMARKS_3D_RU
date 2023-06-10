rem @echo off
echo Updating quadrant data from osm
set WORK_FOLDER=d:\_VFR_LANDMARKS_3D_RU\work_folder
rem SET QUADRANT=+56+038
rem SET BBOX=38,56,39,57
SET QUADRANT=%1
SET BBOX=poly\%~2
set WORK_FOLDER=%WORK_FOLDER%\%QUADRANT%\osm_data
set PLANET=d:\_planet.osm\russia-latest.osm.pbf

echo Quadrant: %QUADRANT%
echo BBOX: %BBOX%
echo Working folder: %WORK_FOLDER%

rem osmium extract -v -p %BBOX% %PLANET% -o %WORK_FOLDER%\%QUADRANT%_new.pbf
rem osmconvert64 %PLANET% -B=%BBOX% --complete-multipolygons -o="%WORK_FOLDER%\%QUADRANT%_new.pbf"


call osmosis --read-pbf file="%PLANET%" --bounding-polygon file="%BBOX%" --write-pbf file="%WORK_FOLDER%\%QUADRANT%_new.pbf"
osmconvert "%WORK_FOLDER%\%QUADRANT%_new.pbf" -o="%WORK_FOLDER%\%QUADRANT%.o5m"
osmconvert "%WORK_FOLDER%\%QUADRANT%_new.pbf" -o="%WORK_FOLDER%\%QUADRANT%.osm"

:end



