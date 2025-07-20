@echo off

rem we compare hashes of .osm files, if it has not changed, we have nothing to do
fc %1.md5 %2\%~nx1.md5 >nul
if %ERRORLEVEL%==0 GOTO :do_nothing

rem SET BLENDER_EXE="c:\Program Files\Blender Foundation\Blender\blender.exe"
SET BLENDER_EXE="c:\Program Files\Blender Foundation\Blender 4.4\blender.exe"

%BLENDER_EXE% --background --python d:\_VFR_LANDMARKS_3D_RU\scripts\osm2obj_b4.py -- %1 %2

rem if blender file is create successfully, let's copy hash file, for future runs
IF EXIST %2\%~n1.blend (
    xcopy /Y /Q %1.md5 %2
	touch %2\%~nx1.md5
)	

IF EXIST %2\%~n1.blend (
	%BLENDER_EXE% --background %2\%~n1.blend --python d:\_VFR_LANDMARKS_3D_RU\scripts\render_building_b4.py
)


GOTO :end
:do_nothing
rem echo lazy work: original file %~nx1 has not changed

:end 

