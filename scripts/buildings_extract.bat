@echo off
set WORK_FOLDER=work_folder\07_building_data
SET SOURCE_FILE="work_folder\00_planet.osm\russia-latest.o5m"

rem echo Working folder: %WORK_FOLDER%
touch %WORK_FOLDER%\.start

osmfilter %SOURCE_FILE% --keep="building=* and ( amenity=place_of_worship or historic=* or wikipedia=* or tourism=attraction or barrier=city_wall or height>90 )" >%WORK_FOLDER%\buildings.osm
osmfilter %SOURCE_FILE% --keep="building=church =cathedral =bell_tower =chapel =shrine =temple =mosque =synagogue tower:type=bell_tower" >%WORK_FOLDER%\churches.osm
osmfilter %SOURCE_FILE% --keep="( man_made=water_tower ) or ( tower:type=defensive =fortification )" >%WORK_FOLDER%\towers.osm
osmfilter %SOURCE_FILE% --keep="( landuse=religious and barrier=fence ) or ( historic=yes and barrier=wall )" >%WORK_FOLDER%\walls2.osm
osmfilter %SOURCE_FILE% --keep="building:part=*" >%WORK_FOLDER%\building_parts.osm

rem chimneys are not used now, but they maybe potentially needed for x-plane, since those are tall objects-all
rem osmfilter %SOURCE_FILE% --keep="man_made=chimney" >%WORK_FOLDER%\chimney.osm

call osmosis --rx %WORK_FOLDER%\buildings.osm --rx %WORK_FOLDER%\churches.osm --rx %WORK_FOLDER%\towers.osm --rx %WORK_FOLDER%\walls2.osm  --merge --merge --merge --wx %WORK_FOLDER%\objects-all.osm
call osmosis --rx %WORK_FOLDER%\objects-all.osm --rx %WORK_FOLDER%\building_parts.osm  --merge --wx %WORK_FOLDER%\objects-with-parts.osm
touch %WORK_FOLDER%\.fin