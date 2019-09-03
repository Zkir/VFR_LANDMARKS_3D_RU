@echo off
set WORK_FOLDER=d:\_VFR_LANDMARKS_3D_RU\work_folder

rem SET QUADRANT=+56+038
SET QUADRANT=%1

set WORK_FOLDER=%WORK_FOLDER%\%QUADRANT%\osm_data

SET SOURCE_FILE="%WORK_FOLDER%\%QUADRANT%.o5m"


echo Quadrant: %QUADRANT%
echo Working folder: %WORK_FOLDER%

md %WORK_FOLDER%

osmfilter %SOURCE_FILE% --keep="amenity=place_of_worship building=church =cathedral =bell_tower =chapel =shrine =temple =mosque =synagogue tower:type=bell_tower" >%WORK_FOLDER%\churches.osm
osmfilter %SOURCE_FILE% --keep="tower:type=defensive =fortification" >%WORK_FOLDER%\towers.osm
osmfilter %SOURCE_FILE% --keep="man_made=chimney" >%WORK_FOLDER%\chimney.osm
osmfilter %SOURCE_FILE% --keep="man_made=water_tower" >%WORK_FOLDER%\water_tower.osm
osmfilter %SOURCE_FILE% --keep="building=* and barrier=city_wall" >%WORK_FOLDER%\walls.osm
osmfilter %SOURCE_FILE% --keep="historic=yes and barrier=wall" >%WORK_FOLDER%\walls2.osm
osmfilter %SOURCE_FILE% --keep="landuse=religious and barrier=fence" >%WORK_FOLDER%\church_fences.osm
osmfilter %SOURCE_FILE% --keep="building:part=*" >%WORK_FOLDER%\building_parts.osm
osmfilter %SOURCE_FILE% --keep="building=* and historic=*" >%WORK_FOLDER%\historic.osm
osmfilter %SOURCE_FILE% --keep="building=* and wikipedia=*" >%WORK_FOLDER%\wikipedia.osm

rem osmfilter %SOURCE_FILE% --keep-nodes="place=*" --keep-ways= --keep-relations=  >%WORK_FOLDER%\geocoder.osm
rem osmfilter %SOURCE_FILE% --keep="boundary=administrative"   >%WORK_FOLDER%\geocoder1.osm

call osmosis --rx %WORK_FOLDER%\churches.osm --rx %WORK_FOLDER%\towers.osm --rx %WORK_FOLDER%\water_tower.osm --rx %WORK_FOLDER%\walls.osm --rx %WORK_FOLDER%\walls2.osm --rx %WORK_FOLDER%\church_fences.osm --rx %WORK_FOLDER%\wikipedia.osm --merge --merge --merge --merge --merge --merge --wx %WORK_FOLDER%\objects-all.osm
call osmosis --rx %WORK_FOLDER%\objects-all.osm --rx %WORK_FOLDER%\building_parts.osm  --merge --wx %WORK_FOLDER%\objects-with-parts.osm
