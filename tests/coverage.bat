@echo off
cd..

CALL .\venv\Scripts\activate.bat

cd src

python -m  pytest --cov-config=../tests/.coveragerc --cov=../src ../tests -p no:warnings > ../tests/coverage.txt

del .coverage