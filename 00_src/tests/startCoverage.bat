@echo off
CALL ..\..\.\venv\Scripts\activate.bat

::pytest tests/ --cov -p no:warnings
pytest tests/ --cov -p no:warnings > coverage.txt
del .coverage