@echo off
SET QUADRANT=%1
SET BBOX=%2

call update %QUADRANT% %BBOX%
call extract %QUADRANT%
OsmParser\main.py %QUADRANT%
echo main.py finished

OsmParser\test.py %QUADRANT%

call upload %QUADRANT%

echo all done