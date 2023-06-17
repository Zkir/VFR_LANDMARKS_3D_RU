@echo off
echo upload quadrant data to web

set WORK_FOLDER=d:\_VFR_LANDMARKS_3D_RU\work_folder
echo Working folder: %WORK_FOLDER%

xcopy /Y /Q %WORK_FOLDER%\30_3dmodels\*.x3d  d:\_VFR_LANDMARKS_3D_RU\3dcheck\models
xcopy /Y /Q %WORK_FOLDER%\30_3dmodels\*.png  d:\_VFR_LANDMARKS_3D_RU\3dcheck\models
rem xcopy /Y /Q %WORK_FOLDER%\30_3dmodels\*.html d:\_VFR_LANDMARKS_3D_RU\3dcheck\models

xcopy /Y /Q %WORK_FOLDER%\10_osm_extracts\*.dat d:\_VFR_LANDMARKS_3D_RU\3dcheck\data
xcopy /Y /Q %WORK_FOLDER%\Quadrants.dat d:\_VFR_LANDMARKS_3D_RU\3dcheck\data


"c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u %WORK_FOLDER%\30_3dmodels\*.x3d   -p /http/models -s
"c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u %WORK_FOLDER%\30_3dmodels\*.png   -p /http/models -s
rem "c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u %WORK_FOLDER%\30_3dmodels\*.html   -p /http/models -s

rem "c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u d:\_VFR_LANDMARKS_3D_RU\3dcheck\%QUADRANT%.html   -p /http/ -s
"c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u d:\_VFR_LANDMARKS_3D_RU\3dcheck\index.html   -p /http/ -s

"c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u %WORK_FOLDER%\10_osm_extracts\*.dat -p /http/data -s
"c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u %WORK_FOLDER%\Quadrants.dat   -p /http/data -s 