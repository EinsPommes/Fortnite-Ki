# Fortnite KI-Agent

Ein fortschrittliches KI-System, das Fortnite auf professionellem Niveau mittels Reinforcement Learning und Computer Vision spielt.

## Funktionen

- Echtzeit-Spielanalyse mittels Computer Vision
- Fortschrittliches Entscheidungssystem für Kampf und Ressourcenmanagement
- Dynamische Strategieanpassung basierend auf der Spielphase
- Professionelle Bau- und Editierfähigkeiten
- Trainingsystem basierend auf Reinforcement Learning

## Voraussetzungen

- Python 3.8 oder höher
- CUDA-fähige Grafikkarte (empfohlen)
- Installiertes Fortnite
- Benötigte Python-Pakete (siehe requirements.txt)

## Installation

1. Repository klonen:
```bash
git clone https://github.com/yourusername/Fortnite-Ki.git
cd Fortnite-Ki
```

2. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

3. Programm starten:
```bash
python src/main.py
```

## Projektstruktur

- `src/environment/`: Spielschnittstelle und Umgebungshandling
- `src/models/`: Neuronale Netzwerkarchitekturen und Agent-Implementierung
- `src/strategies/`: Entscheidungsfindung und Spielstrategien
- `training/`: Trainingsskripte und Konfigurationen
- `utils/`: Hilfsfunktionen und Tools

## Verwendung

1. Stellen Sie sicher, dass Fortnite im Vollbildmodus läuft
2. Führen Sie das Hauptprogramm aus:
```bash
python src/main.py
```
3. Beenden Sie das Programm mit Strg+C

## Training

Der Agent verwendet PPO (Proximal Policy Optimization) für das Training mit folgenden Funktionen:
- Verarbeitung visueller Eingaben mittels CNN
- Angepasste Belohnungsfunktion basierend auf Überlebenszeit, Eliminierungen und Ressourcenmanagement
- Experience Replay für verbessertes Lernen
- Dynamische Schwierigkeitsanpassung während des Trainings

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe LICENSE-Datei für Details.
