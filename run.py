import os
import sys

# Füge den Projektordner zum Python-Pfad hinzu
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Starte die Hauptanwendung
from src.main import main

if __name__ == "__main__":
    main()
