@echo off
SET BLENDER_EXE="c:\Program Files\Blender Foundation\Blender\blender.exe"

rem we compare hashes of .osm files, if it has not changed, we have nothing to do
fc %1.md5 %2\%~nx1.md5 >nul
if %ERRORLEVEL%==0 GOTO :do_nothing

pushd d:\tools\osm2world
REM call osm2world-windows  -i d:\_VFR_LANDMARKS_3D_RU\%~1  -o d:\_VFR_LANDMARKS_3D_RU\%2\%~n1.gltf
call osm2world-windows  -i d:\_VFR_LANDMARKS_3D_RU\%~1  -o d:\_VFR_LANDMARKS_3D_RU\%2\%~n1.obj

IF %ERRORLEVEL% NEQ 0 goto :error
popd 

rem if model file is create successfully, let's copy hash file, for future runs
IF EXIST %2\%~n1.obj (
    xcopy /Y /Q %1.md5 %2
	touch %2\%~nx1.md5
)

%BLENDER_EXE% --background --python d:\_VFR_LANDMARKS_3D_RU\scripts\obj2obj.py -- d:\_VFR_LANDMARKS_3D_RU\%2\%~n1.obj %2

scripts\obj2x3d.py "d:\_VFR_LANDMARKS_3D_RU\%2\%~n1.obj"

GOTO :end
:error
popd 
echo some error has occured
exit 1
:do_nothing
rem echo lazy work: original file %~nx1 has not changed

:end 


