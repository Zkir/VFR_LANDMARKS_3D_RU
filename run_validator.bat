@echo off
set lockfile=work_folder\.lock
rem ========== protection from running the process twice ===
IF EXIST %lockfile% goto error
touch %lockfile%
rem ========== main part ===================================

make planet-update > work_folder\log.txt 2>&1
make   >> work_folder\log.txt 2>&1

rem ========== tail ========================================
del %lockfile%
echo process complete >> work_folder\log.txt 2>&1
echo process complete 
goto end
:error 
echo process is already running

:end