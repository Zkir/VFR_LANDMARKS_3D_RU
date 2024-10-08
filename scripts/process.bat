@echo off
rem this script is used to (partially) process a single quadrant without makefile
SET QUADRANT=%1
SET BBOX=%2

rem call update2 RU
rem if errorlevel 1 goto error

call scripts\buildings_extract-per-region %QUADRANT% %QUADRANT%.poly
if errorlevel 1 goto error

IF NOT EXIST work_folder\20_osm_3dmodels mkdir work_folder\20_osm_3dmodels
IF NOT EXIST work_folder\21_osm_objects_list mkdir work_folder\21_osm_objects_list


OsmParser\main.py %QUADRANT%
if errorlevel 1 goto error

OsmParser\wikidata.py update-region -i work_folder\21_osm_objects_list\%QUADRANT%.dat -r
if errorlevel 1 goto error

call scripts\upload.bat

echo all done

goto end
:error
echo.
echo ERROR: unable to process quadrant!
:end