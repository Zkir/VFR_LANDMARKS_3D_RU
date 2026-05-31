@echo off
rem Script to export Blender file to X-Plane OBJ
SET BLENDER_EXE="c:\Program Files\Blender Foundation\Blender 5.1\blender.exe"

echo Exporting %1
%BLENDER_EXE% --background %1 --python d:\_VFR_LANDMARKS_3D_RU\scripts\export_xplane.py
