@echo off
SET SOURCE_FILE=russia-latest.o5m
SET WORK_FOLDER=d:\_planet.osm
cd %WORK_FOLDER%

osmfilter %SOURCE_FILE% --keep="place=city or place=town or place=village or place=hamlet"  >%WORK_FOLDER%\geocoder_place.osm
osmfilter %SOURCE_FILE% --keep="boundary=administrative"   >%WORK_FOLDER%\geocoder_boundary.osm


call osmosis --rx %WORK_FOLDER%\geocoder_place.osm --rx %WORK_FOLDER%\geocoder_boundary.osm --merge --wx %WORK_FOLDER%\geocoder.osm
