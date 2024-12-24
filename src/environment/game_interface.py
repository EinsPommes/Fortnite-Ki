import cv2
import numpy as np
from mss import mss
import torch

class FortniteInterface:
    def __init__(self, screen_region=None):
        self.screen_capture = mss()
        self.screen_region = screen_region or {"top": 0, "left": 0, "width": 1920, "height": 1080}
        self.default_state = {
            "health": 100,
            "shield": 0,
            "materials": {
                "wood": 0,
                "stone": 0,
                "metal": 0
            },
            "weapons": [],
            "position": [0, 0],
            "players_alive": 100,
            "zone_size": 1.0,
            "height": 0
        }
        
    def get_game_state(self):
        """Capture and process the current game screen."""
        screenshot = self.screen_capture.grab(self.screen_region)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        # Skaliere das Bild auf die gewünschte Größe
        frame = cv2.resize(frame, (480, 270))
        return frame
    
    def detect_objects(self, frame):
        """Detect players, buildings, and items in the frame."""
        # Dummy-Implementierung für Testzwecke
        return {
            "players": [],
            "buildings": [],
            "items": []
        }
    
    def get_player_state(self):
        """Get current player state (health, shields, materials, etc.)."""
        # Dummy-Implementierung für Testzwecke
        return self.default_state.copy()
    
    def get_game_phase(self):
        """Determine current game phase (early, mid, late game)."""
        # Dummy-Implementierung für Testzwecke
        return "early"

    def process_frame(self, frame):
        """Verarbeite den Frame für die KI-Eingabe."""
        # Konvertiere zu Graustufen für einfachere Verarbeitung
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # Normalisiere die Werte zwischen 0 und 1
        normalized = gray.astype(np.float32) / 255.0
        return normalized
