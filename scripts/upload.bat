@echo off
echo upload quadrant data to web

set WORK_FOLDER=d:\_VFR_LANDMARKS_3D_RU\work_folder
echo Working folder: %WORK_FOLDER%

xcopy /Y /Q %WORK_FOLDER%\30_3dmodels\*.x3d  d:\_VFR_LANDMARKS_3D_RU\3dcheck\models
xcopy /Y /Q %WORK_FOLDER%\30_3dmodels\*.png  d:\_VFR_LANDMARKS_3D_RU\3dcheck\models

xcopy /Y /Q %WORK_FOLDER%\21_osm_objects_list\*.dat d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\quadrants
xcopy /Y /Q %WORK_FOLDER%\22_all_osm_objects_list\RUS_TOP.dat d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\quadrants
xcopy /Y /Q %WORK_FOLDER%\22_all_osm_objects_list\RUS_TOP_WINDOWS.dat d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\quadrants

xcopy /Y /Q %WORK_FOLDER%\22_all_osm_objects_list\RUS_LATEST.dat d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\quadrants
xcopy /Y /Q %WORK_FOLDER%\22_all_osm_objects_list\recent_activity.png d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\images
xcopy /Y /Q %WORK_FOLDER%\Quadrants.dat d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\quadrants

xcopy /Y /Q %WORK_FOLDER%\20_osm_3dmodels\*.errors.dat  d:\_VFR_LANDMARKS_3D_RU\3dcheck\data\errors


rem "c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u %WORK_FOLDER%\30_3dmodels\*.x3d   -p /http/models -s
rem "c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u %WORK_FOLDER%\30_3dmodels\*.png   -p /http/models -s
rem "c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u d:\_VFR_LANDMARKS_3D_RU\3dcheck\index.html   -p /http/ -s
rem "c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u %WORK_FOLDER%\11_osm_objects_list\*.dat -p /http/data -s
rem "c:\Program Files\CoreFTP\coreftp.exe" -site 3dcheck -O -u %WORK_FOLDER%\Quadrants.dat   -p /http/data -s 