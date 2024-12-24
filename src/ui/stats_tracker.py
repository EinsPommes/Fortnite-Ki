import numpy as np
from collections import deque

class StatsTracker:
    def __init__(self, max_history=100):
        self.max_history = max_history
        self.reset()
        
    def reset(self):
        """Setze alle Statistiken zurück."""
        self.kills = 0
        self.matches_played = 0
        self.placement_history = deque(maxlen=self.max_history)
        self.kills_history = deque(maxlen=self.max_history)
        self.current_placement = 100
        
    def update_placement(self, new_placement):
        """Aktualisiere die aktuelle Platzierung."""
        self.current_placement = new_placement
        
    def end_match(self):
        """Beende das aktuelle Match und aktualisiere die Statistiken."""
        self.placement_history.append(self.current_placement)
        self.kills_history.append(self.kills)
        self.matches_played += 1
        self.kills = 0
        self.current_placement = 100
        
    def add_kill(self):
        """Füge eine Eliminierung hinzu."""
        self.kills += 1
        
    def get_stats(self):
        """Hole die aktuellen Statistiken."""
        return {
            'current_kills': self.kills,
            'current_placement': self.current_placement,
            'avg_placement': np.mean(self.placement_history) if self.placement_history else 0,
            'avg_kills': np.mean(self.kills_history) if self.kills_history else 0,
            'matches_played': self.matches_played,
            'total_kills': sum(self.kills_history),
        }
