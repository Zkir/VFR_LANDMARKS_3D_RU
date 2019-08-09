@echo off
rem update +56+038 38,56,39,57
rem update +55+037 "37,55,38,56"
rem update +52+041 41,52,42,53
call update +59+030 "30,59,31,60"
call extract +59+030
OsmParser/main.py +59+030
OsmParser/test.py +59+030