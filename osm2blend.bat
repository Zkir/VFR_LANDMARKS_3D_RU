@echo off
SET BLENDER_EXE="c:\Program Files\Blender Foundation\Blender\blender.exe"
%BLENDER_EXE% --background --python d:\_VFR_LANDMARKS_3D_RU\osm2obj.py -- %1 
echo %errorlevel%

rem obj2x3d.py %1 
rem echo %errorlevel%
