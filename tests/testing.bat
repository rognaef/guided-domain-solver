@echo off
cd..

CALL .\venv\Scripts\activate.bat

cd src

python -m pytest ../tests -v -W ignore::DeprecationWarning

pause >nul