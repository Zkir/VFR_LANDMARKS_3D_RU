@echo off
cls
echo 3dcheck validator (c)zkir 2019
echo starting process
:restart
del /q osmupdate_temp\*.*
del /q d:\_planet.osm\osmupdate_temp\*.*
cd d:\_planet.osm\
call d:\_planet.osm\update.bat
if errorlevel 1 goto error
cd d:\_VFR_LANDMARKS_3D_RU\

osmparser\planner.py
if errorlevel 1 goto error

echo cycle completed, starting new one
goto restart
:error
echo.
echo ERROR: unable to process quadrant!
:end