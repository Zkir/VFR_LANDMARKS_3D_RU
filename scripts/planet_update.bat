@echo off
echo Updating planet osm
SET WORK_FOLDER=%1
cd %WORK_FOLDER%


osmupd "russia-latest.osm.pbf" "russia-latest-latest.osm.pbf" -B=russia.poly -v --keep-tempfiles
if errorlevel 1 goto error
rem if update was successful, we can delete the old file and rename the new one as old one.
del "russia-latest.osm.pbf"
ren "russia-latest-latest.osm.pbf" "russia-latest.osm.pbf
echo osm.pbf updated

osmconvert "russia-latest.osm.pbf" -o="russia-latest.o5m"
if errorlevel 1 goto error

goto end
:error
echo.
echo ERROR HAS OCCURED!!!
Exit/b 1
:end


