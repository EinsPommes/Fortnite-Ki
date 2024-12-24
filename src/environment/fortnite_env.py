import gymnasium as gym
from gymnasium import spaces
import numpy as np
from src.environment.game_interface import FortniteInterface
from src.controls.game_controls import FortniteControls
from src.vision.object_detection import FortniteVision
from src.strategies.decision_maker import DecisionMaker, GamePhase

class FortniteEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render_modes': ['human'], 'render.modes': ['human']}

    def __init__(self):
        super(FortniteEnv, self).__init__()
        
        # Initialisiere Komponenten
        self.game_interface = FortniteInterface()
        self.controls = FortniteControls()
        self.vision = FortniteVision()
        self.decision_maker = DecisionMaker()
        
        # Definition des Aktionsraums
        # [vorwärts, rückwärts, links, rechts, springen, schießen, bauen, editieren]
        self.action_space = spaces.MultiDiscrete([2] * 8)
        
        # Definition des Beobachtungsraums
        self.observation_space = spaces.Box(
            low=0, 
            high=255,
            shape=(270, 480, 3),  # Skalierte Bildgröße
            dtype=np.uint8
        )
        
        self.current_step = 0
        self.max_steps = 1000
        self.last_health = 100
        self.last_shield = 0
        self.elimination_count = 0
        
    def step(self, action):
        self.current_step += 1
        
        # Führe Aktion aus
        self.controls.perform_action(action)
        
        # Hole neuen Spielzustand
        frame = self.game_interface.get_game_state()
        vision_data = self.vision.process_frame(frame)
        
        # Aktualisiere Spielzustand
        current_health = vision_data['health']
        current_shield = vision_data['shield']
        players_nearby = len(vision_data['players'])
        
        # Berechne Belohnung
        reward = self._calculate_reward(
            current_health, 
            current_shield,
            vision_data
        )
        
        # Aktualisiere gespeicherte Werte
        self.last_health = current_health
        self.last_shield = current_shield
        
        # Überprüfe, ob Episode beendet ist
        done = self._is_done(current_health)
        
        # Erstelle Info-Dictionary
        info = {
            'vision_data': vision_data,
            'step': self.current_step,
            'players_nearby': players_nearby
        }
        
        return frame, reward, done, False, info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        self.last_health = 100
        self.last_shield = 0
        self.elimination_count = 0
        
        # Hole initialen Zustand
        frame = self.game_interface.get_game_state()
        vision_data = self.vision.process_frame(frame)
        
        info = {
            'vision_data': vision_data,
            'step': self.current_step
        }
        
        return frame, info

    def _calculate_reward(self, current_health, current_shield, vision_data):
        """Berechne die Belohnung basierend auf verschiedenen Faktoren."""
        reward = 0.0
        
        # Überlebensbelohnung
        reward += 0.1
        
        # Gesundheits- und Schildänderung
        health_change = current_health - self.last_health
        shield_change = current_shield - self.last_shield
        reward += (health_change + shield_change) * 0.5
        
        # Belohnung für Eliminierungen
        if self.elimination_count > 0:
            reward += self.elimination_count * 10
            self.elimination_count = 0
        
        # Bestrafung für riskante Situationen
        players_nearby = len(vision_data['players'])
        if players_nearby > 2:  # Mehr als 2 Gegner in der Nähe
            reward -= 0.2
            
        # Zonenposition
        if not vision_data['zone'].get('in_zone', True):
            reward -= 0.3
            
        return reward

    def _is_done(self, current_health):
        """Überprüfe, ob die Episode beendet ist."""
        if current_health <= 0:
            return True
        if self.current_step >= self.max_steps:
            return True
        return False

    def render(self, mode='human'):
        """Optional: Implementiere Rendering für Debugging."""
        pass

    def close(self):
        """Cleanup am Ende."""
        pass
