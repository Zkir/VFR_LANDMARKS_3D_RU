@echo off
SET QUADRANT=%1
SET BBOX=%2

call update %QUADRANT% %BBOX%
if errorlevel 1 goto error

call extract %QUADRANT%
if errorlevel 1 goto error

OsmParser\main.py %QUADRANT%
if errorlevel 1 goto error

echo all done

goto end
:error
echo.
echo ERROR: unable to process quadrant!
:end