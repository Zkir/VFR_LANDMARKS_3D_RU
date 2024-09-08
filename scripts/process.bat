@echo off
rem this script is used to (partially) process a single quadrant without makefile
SET QUADRANT=%1
SET BBOX=%2

rem call update2 RU
rem if errorlevel 1 goto error

call scripts\buildings_extract-per-region %QUADRANT% %QUADRANT%.poly
if errorlevel 1 goto error

OsmParser\main.py %QUADRANT%
if errorlevel 1 goto error

call upload.bat

echo all done

goto end
:error
echo.
echo ERROR: unable to process quadrant!
:end