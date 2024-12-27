rem @echo off
echo Updating planet osm
SET WORK_FOLDER=%1
SET COUNTRY=planet
cd %WORK_FOLDER%


osmupd "%COUNTRY%-latest.osm.pbf" "%COUNTRY%-latest-latest.osm.pbf"  -v 
rem -B=%COUNTRY%.poly
if errorlevel 1 goto error
rem if update was successful, we can delete the old file and rename the new one as old one.
del "%COUNTRY%-latest.osm.pbf"
ren "%COUNTRY%-latest-latest.osm.pbf" "%COUNTRY%-latest.osm.pbf

echo osm.pbf updated

osmconvert "%COUNTRY%-latest.osm.pbf" -o="%COUNTRY%-latest.o5m"
if errorlevel 1 goto error

goto end
:error
echo.
echo ERROR HAS OCCURED!!!
Exit/b 1
:end


