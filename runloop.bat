@echo off


:run
cls
SET input=
python skytower/game.py
echo [Enter] to re-run. Any other input exits.
set /P input=""
if ([%input%]) NEQ ([]) goto end
goto run

:end