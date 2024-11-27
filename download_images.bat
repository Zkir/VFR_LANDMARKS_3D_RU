@echo off
:restart
make work_folder\25_images\extract_images
if errorlevel 1 goto restart