from enum import Enum
import numpy as np
import math

class GamePhase(Enum):
    EARLY = "early"
    MID = "mid"
    LATE = "late"

class DecisionMaker:
    def __init__(self):
        self.current_phase = GamePhase.EARLY
        self.min_materials = 500  # Mindestmenge an Materialien
        self.safe_distance = 50   # Sicherer Abstand zu Gegnern
        self.aggressive_distance = 20  # Abstand für aggressives Spiel
        
    def update_game_phase(self, players_alive, zone_size):
        """Update the current game phase based on game state."""
        if players_alive > 50 and zone_size > 0.7:
            self.current_phase = GamePhase.EARLY
        elif players_alive > 15:
            self.current_phase = GamePhase.MID
        else:
            self.current_phase = GamePhase.LATE
            
    def evaluate_combat_engagement(self, player_state, enemy_state):
        """Entscheide, ob ein Kampf begonnen werden soll."""
        # Faktoren für die Entscheidung
        health_advantage = (player_state["health"] + player_state["shield"]) > (enemy_state.get("health", 100) + enemy_state.get("shield", 0))
        position_advantage = player_state["height"] > enemy_state.get("height", 0)
        resource_advantage = sum(player_state["materials"].values()) > self.min_materials
        
        # Gewichtung je nach Spielphase
        if self.current_phase == GamePhase.EARLY:
            # Früh im Spiel: Sehr vorsichtig
            return all([health_advantage, position_advantage, resource_advantage])
        elif self.current_phase == GamePhase.MID:
            # Mittleres Spiel: Ausgeglichener
            return sum([health_advantage, position_advantage, resource_advantage]) >= 2
        else:
            # Endgame: Aggressiver
            return any([health_advantage, position_advantage])
    
    def get_build_strategy(self, combat_state):
        """Bestimme die optimale Baustrategie."""
        if combat_state["under_fire"]:
            return {
                "type": "defensive_build",
                "structures": ["wall", "ramp", "floor"],
                "pattern": "box"
            }
        elif combat_state["attacking"]:
            return {
                "type": "aggressive_build",
                "structures": ["ramp", "wall"],
                "pattern": "push"
            }
        return {
            "type": "basic_build",
            "structures": ["wall"],
            "pattern": "single"
        }
    
    def get_rotation_strategy(self, current_pos, zone_info, players):
        """Plane den optimalen Rotationsweg."""
        zone_center = zone_info["center"]
        zone_radius = zone_info["radius"]
        
        # Berechne Distanz zur Zone
        distance_to_zone = math.sqrt(
            (current_pos[0] - zone_center[0])**2 + 
            (current_pos[1] - zone_center[1])**2
        )
        
        # Finde sichere Wege (vermeide Gegner)
        safe_paths = self._find_safe_paths(current_pos, zone_center, players)
        
        if distance_to_zone > zone_radius:
            # Außerhalb der Zone: Direkter Weg
            return {
                "type": "direct",
                "target": zone_center,
                "priority": "speed"
            }
        else:
            # Innerhalb der Zone: Strategische Position
            return {
                "type": "strategic",
                "target": self._find_strategic_position(zone_center, players),
                "priority": "safety"
            }
    
    def _find_safe_paths(self, start, end, players):
        """Finde sichere Wege unter Berücksichtigung von Gegnerpositionen."""
        safe_paths = []
        # TODO: Implementiere Pathfinding-Algorithmus
        return safe_paths
    
    def _find_strategic_position(self, zone_center, players):
        """Finde eine strategisch günstige Position."""
        # Suche erhöhte Position nahe des Zonenzentrums
        strategic_pos = zone_center.copy()
        
        # TODO: Implementiere Positionsanalyse
        return strategic_pos
    
    def get_action_weights(self, game_state):
        """Berechne Gewichtungen für verschiedene Aktionen."""
        weights = {
            "build": 0.0,
            "fight": 0.0,
            "rotate": 0.0,
            "farm": 0.0,
            "heal": 0.0
        }
        
        # Gewichte basierend auf Spielzustand anpassen
        if game_state["health"] < 50:
            weights["heal"] = 0.8
            weights["fight"] = 0.1
        
        if sum(game_state["materials"].values()) < self.min_materials:
            weights["farm"] = 0.7
            
        if game_state["in_combat"]:
            weights["build"] = 0.6
            weights["fight"] = 0.4
            
        if not game_state["in_zone"]:
            weights["rotate"] = 0.9
            
        return weights
