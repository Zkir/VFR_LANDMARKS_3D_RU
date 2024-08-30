@echo off
set lockfile=work_folder\.lock
rem ========== protection from running the process twice ===
IF EXIST %lockfile% goto error
touch %lockfile%
rem ========== main part ===================================

make planet-update
make 

rem ========== tail ========================================
del %lockfile%
echo process complete 
goto end
:error 
echo process is already running

:end