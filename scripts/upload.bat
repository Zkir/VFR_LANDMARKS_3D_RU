@echo off
echo upload quadrant data to web

set WORK_FOLDER=d:\_VFR_LANDMARKS_3D_RU\work_folder
echo Working folder: %WORK_FOLDER%

IF NOT EXIST d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\models mkdir d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\models
xcopy /Y /Q %WORK_FOLDER%\30_3dmodels\*.x3d  d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\models
xcopy /Y /Q %WORK_FOLDER%\30_3dmodels\*.png  d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\models

IF NOT EXIST d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\errors mkdir d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\errors
xcopy /Y /Q %WORK_FOLDER%\20_osm_3dmodels\*.errors.dat  d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\errors

xcopy /Y /Q %WORK_FOLDER%\Quadrants.dat d:\_VFR_LANDMARKS_3D_RU\3dcheck\data

IF NOT EXIST d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\world mkdir d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\world
xcopy /Y /Q /s %WORK_FOLDER%\22_all_osm_objects_list\world d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\world
IF NOT EXIST d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\countries mkdir d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\countries
xcopy /Y /Q /s %WORK_FOLDER%\22_all_osm_objects_list\countries d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\countries




rem "c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u %WORK_FOLDER%\30_3dmodels\*.x3d   -p /http/models -s
rem "c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u %WORK_FOLDER%\30_3dmodels\*.png   -p /http/models -s
rem "c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u d:\_VFR_LANDMARKS_3D_RU\3dcheck\index.html   -p /http/ -s
rem "c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u %WORK_FOLDER%\11_osm_objects_list\*.dat -p /http/data -s
rem "c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u %WORK_FOLDER%\Quadrants.dat   -p /http/data -s 