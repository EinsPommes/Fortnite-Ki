import os
import sys

# Füge den Projektordner zum Python-Pfad hinzu
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from PyQt6.QtWidgets import QApplication
from src.environment.game_interface import FortniteInterface
from src.models.agent import FortniteAgent
from src.strategies.decision_maker import DecisionMaker
from src.ui.main_window import MainWindow
from src.ui.stats_tracker import StatsTracker

class FortniteAI:
    def __init__(self):
        # Initialisiere Komponenten
        self.game_interface = FortniteInterface()
        self.decision_maker = DecisionMaker()
        
        # Konfiguriere den AI Agent
        STATE_DIM = 512
        ACTION_DIM = 8
        self.agent = FortniteAgent(state_dim=STATE_DIM, action_dim=ACTION_DIM)
        
        # Statistik-Tracker
        self.stats = StatsTracker()
        
        # Lade ein vortrainiertes Modell, falls vorhanden
        self.model_path = os.path.join("models", "trained_model.zip")
        if os.path.exists(self.model_path):
            print("Lade trainiertes Modell...")
            self.agent.load_model(self.model_path)
        
    def process_frame(self, frame):
        """Verarbeite einen Frame und erhalte die nächste Aktion."""
        action = self.agent.get_action(frame)
        return action
        
    def save_model(self):
        """Speichere das aktuelle Modell."""
        os.makedirs("models", exist_ok=True)
        self.agent.save_model(self.model_path)
        print("Modell gespeichert")

def main():
    # Erstelle die Qt-Anwendung
    app = QApplication(sys.argv)
    
    # Erstelle das Hauptfenster
    window = MainWindow()
    window.show()
    
    # Erstelle die Fortnite-KI
    ai = FortniteAI()
    
    # Verbinde UI-Signale mit KI-Funktionen
    window.save_button.clicked.connect(ai.save_model)
    
    def update_ui():
        if window.ai_running:
            # Hole den aktuellen Frame
            frame = ai.game_interface.get_game_state()
            
            # Verarbeite den Frame mit der KI
            if window.training_mode:
                # TODO: Implementiere Trainingsmodus
                pass
            else:
                action = ai.process_frame(frame)
            
            # Aktualisiere die UI
            window.update_game_view(frame)
            
            # Hole aktuelle Statistiken
            stats = ai.stats.get_stats()
            window.update_stats(
                stats['current_kills'],
                stats['current_placement'],
                stats['avg_placement']
            )
    
    # Verbinde Update-Funktion mit dem UI-Timer
    window.update_timer.timeout.connect(update_ui)
    
    # Starte die Anwendung
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
