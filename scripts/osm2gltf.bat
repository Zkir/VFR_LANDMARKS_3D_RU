@echo off

rem we compare hashes of .osm files, if it has not changed, we have nothing to do
fc %1.md5 %2\%~nx1.md5 >nul
if %ERRORLEVEL%==0 GOTO :do_nothing

pushd d:\tools\osm2world
call osm2world-windows  -i d:\_VFR_LANDMARKS_3D_RU\%~1  -o d:\_VFR_LANDMARKS_3D_RU\%2\%~n1.gltf
IF %ERRORLEVEL% NEQ 0 goto :error
popd 

rem if model file is create successfully, let's copy hash file, for future runs
IF EXIST %2\%~n1.gltf (
    xcopy /Y /Q %1.md5 %2
	touch %2\%~nx1.md5
)	
GOTO :end
:error
popd 
echo some error has occured
exit /b 1234
:do_nothing
rem echo lazy work: original file %~nx1 has not changed

:end 

