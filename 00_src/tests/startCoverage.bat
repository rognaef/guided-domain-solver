@echo off
cd..

CALL ..\venv\Scripts\activate.bat

python -m  pytest --cov-config=tests/.coveragerc --cov -p no:warnings > tests/coverage.txt

del .coverage