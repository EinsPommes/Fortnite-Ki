import cv2
import numpy as np
from ultralytics import YOLO
import pytesseract
import torch

class FortniteVision:
    def __init__(self):
        # Lade das vortrainierte YOLO-Modell
        self.model = YOLO('yolov8n.pt')
        
        # Definiere die relevanten Klassen für Fortnite
        self.fortnite_classes = [
            'person', 'car', 'truck', 'boat',  # Bewegliche Objekte
            'backpack', 'umbrella', 'handbag',  # Items
            'sports ball', 'bottle'  # Andere relevante Objekte
        ]
        
        # OCR für Textererkennung (Gesundheit, Munition, etc.)
        self.tesseract_config = '--psm 7'
        
    def detect_objects(self, frame):
        """Erkenne Objekte im Frame mit YOLO."""
        results = self.model(frame)
        
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                if self.model.names[class_id] in self.fortnite_classes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    confidence = float(box.conf[0])
                    detections.append({
                        'class': self.model.names[class_id],
                        'box': [x1, y1, x2, y2],
                        'confidence': confidence
                    })
                    
        return detections
    
    def read_game_text(self, frame, region):
        """Lese Text aus einem bestimmten Bereich des Frames."""
        # Extrahiere Region
        roi = frame[region[1]:region[3], region[0]:region[2]]
        
        # Vorverarbeitung für bessere OCR
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # OCR
        text = pytesseract.image_to_string(thresh, config=self.tesseract_config)
        return text.strip()
    
    def get_health_and_shield(self, frame):
        """Extrahiere Gesundheits- und Schildwerte."""
        # Definiere Regionen für Gesundheit und Schild
        health_region = [50, 50, 150, 80]  # Beispielkoordinaten
        shield_region = [50, 90, 150, 120]  # Beispielkoordinaten
        
        health_text = self.read_game_text(frame, health_region)
        shield_text = self.read_game_text(frame, shield_region)
        
        try:
            health = int(health_text) if health_text.isdigit() else 100
            shield = int(shield_text) if shield_text.isdigit() else 0
        except:
            health, shield = 100, 0
            
        return health, shield
    
    def detect_players(self, frame):
        """Speziell für Spielererkennung optimierte Funktion."""
        detections = self.detect_objects(frame)
        players = [d for d in detections if d['class'] == 'person']
        
        # Sortiere nach Entfernung (Größe der Bounding Box)
        players.sort(key=lambda x: (x['box'][2] - x['box'][0]) * (x['box'][3] - x['box'][1]), reverse=True)
        
        return players
    
    def get_zone_info(self, frame):
        """Extrahiere Informationen über die Sturmzone."""
        # TODO: Implementiere Zonenerkennung
        # Dies würde eine spezielle Bildverarbeitung für die Minimap erfordern
        return {
            'center': [960, 540],  # Bildschirmmitte als Standardwert
            'radius': 1000,
            'moving': False
        }
    
    def process_frame(self, frame):
        """Verarbeite einen Frame vollständig."""
        # Skaliere den Frame für bessere Performance
        frame = cv2.resize(frame, (960, 540))
        
        # Sammle alle relevanten Informationen
        players = self.detect_players(frame)
        health, shield = self.get_health_and_shield(frame)
        zone_info = self.get_zone_info(frame)
        
        return {
            'players': players,
            'health': health,
            'shield': shield,
            'zone': zone_info
        }
