import torch
import torch.nn as nn
import torch.nn.functional as F

class VisualEncoder(nn.Module):
    def __init__(self):
        super(VisualEncoder, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)
        
    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        return x.view(x.size(0), -1)

class PolicyNetwork(nn.Module):
    def __init__(self, input_dim, action_dim):
        super(PolicyNetwork, self).__init__()
        self.visual_encoder = VisualEncoder()
        
        self.fc1 = nn.Linear(input_dim, 512)
        self.fc2 = nn.Linear(512, 256)
        self.action_head = nn.Linear(256, action_dim)
        self.value_head = nn.Linear(256, 1)
        
    def forward(self, state):
        x = self.visual_encoder(state)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        
        action_probs = F.softmax(self.action_head(x), dim=-1)
        state_value = self.value_head(x)
        
        return action_probs, state_value
