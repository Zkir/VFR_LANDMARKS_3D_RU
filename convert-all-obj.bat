@echo off
for %%v in (*.osm) do call d:\_VFR_LANDMARKS_3D_RU\osm2blend.bat "%%v"
