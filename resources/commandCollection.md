# Command Collection

## Virtuelle Umgebung Python
Befehl | Beschreibung
----|----
python -m venv NAME	            |   Erstellen einer vrituellen Umgebung mit dem Namen "NAME"
venv\Scripts\activate.bat	    |   Startet virtuelle Umgebung mit dem Namen "venv" in Windows (falls erfolgreich ->"(venv)" vor dem Pfad)
deactivate					    |	Beendet die virtuelle Umgebung
pip list					    |	Listet alle installierten Bibliotheken der Umgebung
pip freeze > requirements.txt	|	Erstellt requirements.txt File
pip install -r requirements.txt	|	Installiert alle Requirements

## Tests
Befehl | Beschreibung
----|----
pytest								                        |   Startet Tests
pytest -v							                        |   Detailiertere Ausgabe der Tests (noch detailierter mit -vv)
pytest --cov > coverage.txt; Remove-Item -Path .coverage	|   (Powershell) Bewertet die Test Coverage und speichert Ergebnis in coverage.txt und löschen der Meta-Daten

## LLM with Ollama (https://ollama.com)
Befehl | Beschreibung
----|----
ollama pull qwen2.5-coder:7b    |   Ladet das Model "qwen2.5-coder:7b" herunter und speichert es lokal 
ollama run qwen2.5-coder:7b	    |   Lokales Prompten vom Model "qwen2.5-coder:7b"
