@echo off
set lockfile=work_folder\.lock
rem ========== protection from running the process twice ===
IF EXIST %lockfile% goto error_already_running
touch %lockfile%
rem ========== main part ===================================

make planet-update > work_folder\log.txt 2>&1
if errorlevel 1 goto error
make   >> work_folder\log.txt 2>&1
if errorlevel 1 goto error

rem ========== tail ========================================
del %lockfile%
echo process complete >> work_folder\log.txt 2>&1
echo process complete 
goto end

:error_already_running
echo process is already running
goto end

:error 
echo error has occured. sorry. 

:end