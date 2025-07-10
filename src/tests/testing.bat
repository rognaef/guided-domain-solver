@echo off
cd..

CALL ..\venv\Scripts\activate.bat

python -m pytest ../00_src -v -W ignore::DeprecationWarning

pause >nul