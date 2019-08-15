@echo off
echo upload quadrant data to web

SET QUADRANT=%1
set WORK_FOLDER=d:\_VFR_LANDMARKS_3D_RU\work_folder


echo Quadrant: %QUADRANT%
echo Working folder: %WORK_FOLDER%



xcopy /Y %WORK_FOLDER%\%QUADRANT%\osm_3dmodels\*.x3d  d:\_VFR_LANDMARKS_3D_RU\3dcheck\models
xcopy /Y %WORK_FOLDER%\%QUADRANT%\osm_3dmodels\*.png  d:\_VFR_LANDMARKS_3D_RU\3dcheck\models
xcopy /Y %WORK_FOLDER%\%QUADRANT%\osm_3dmodels\*.html d:\_VFR_LANDMARKS_3D_RU\3dcheck\models

xcopy /Y %WORK_FOLDER%\%QUADRANT%\%QUADRANT%.dat d:\_VFR_LANDMARKS_3D_RU\3dcheck\data
xcopy /Y %WORK_FOLDER%\Quadrants.dat d:\_VFR_LANDMARKS_3D_RU\3dcheck\data


"c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u %WORK_FOLDER%\%QUADRANT%\osm_3dmodels\*.x3d   -p /http/models -s
"c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u %WORK_FOLDER%\%QUADRANT%\osm_3dmodels\*.png   -p /http/models -s
"c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u %WORK_FOLDER%\%QUADRANT%\osm_3dmodels\*.html   -p /http/models -s

"c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u d:\_VFR_LANDMARKS_3D_RU\3dcheck\%QUADRANT%.html   -p /http/ -s
"c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u d:\_VFR_LANDMARKS_3D_RU\3dcheck\index.html   -p /http/ -s