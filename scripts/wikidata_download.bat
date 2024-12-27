@echo off
pushd %WORK_FOLDER%
SET WORK_FOLDER=%1
echo download wikidata
aria2c https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2
goto end 

:end
popd