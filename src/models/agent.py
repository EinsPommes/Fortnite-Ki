import torch
import torch.nn as nn
import numpy as np
from stable_baselines3 import PPO
from src.environment.fortnite_env import FortniteEnv

class FortniteAgent:
    def __init__(self, state_dim, action_dim):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Erstelle die Fortnite-Umgebung
        self.env = FortniteEnv()
        
        # Initialisiere PPO model mit der benutzerdefinierten Umgebung
        self.model = PPO(
            "CnnPolicy",
            self.env,
            verbose=1,
            device=self.device,
            learning_rate=3e-4,
        )
        
    def get_action(self, state):
        """Determine the next action based on current state."""
        action, _ = self.model.predict(state, deterministic=True)
        return action
    
    def train(self, total_timesteps=1000000):
        """Train the agent using PPO."""
        self.model.learn(total_timesteps=total_timesteps)
        
    def save_model(self, path):
        """Save the trained model."""
        self.model.save(path)
        
    def load_model(self, path):
        """Load a trained model."""
        self.model = PPO.load(path, env=self.env)
