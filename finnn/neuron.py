"""
FINNN - Fractal Icosahedral Neural Networks Novabene
Neurone e Layer addestrabile
"""

import sys
from pathlib import Path

try:
    current_dir = Path(__file__).parent
except NameError:
    current_dir = Path.cwd()

# Aggiungi la directory genitore (Novae) al path per trovare novabene/
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

import numpy as np
import torch
import torch.nn as nn

from novabene.graph import build_hamiltonian


class FINNNNeuron:
    """Neurone con pesi derivati dall'Hamiltoniana di Dirac sul grafo icosaedrico."""
    
    def __init__(self, lambda_val=0.5, hidden_dim=52):
        self.H = build_hamiltonian(mass_center=lambda_val * 1)
        self.W = np.real(self.H)
        self.bias = np.zeros(hidden_dim, dtype=complex)
        self.activation = lambda x: np.tanh(x)

    def forward(self, input_vector):
        pre_act = self.W @ input_vector + self.bias
        return self.activation(pre_act)

    def evolve(self, steps=10):
        state = np.random.randn(52) + 1j * np.random.randn(52)
        state /= np.linalg.norm(state)
        for _ in range(steps):
            state = self.activation(self.W @ state)
        return state


class FINNNLayer(nn.Module):
    """Layer PyTorch addestrabile con pesi inizializzati dall'Hamiltoniana."""
    
    def __init__(self, lambda_val=0.5):
        super().__init__()
        H = build_hamiltonian(mass_center=lambda_val * 1)
        self.W = nn.Parameter(torch.from_numpy(np.real(H)).float())
        self.bias = nn.Parameter(torch.zeros(52, dtype=torch.float32))

    def forward(self, x):
        return torch.tanh(torch.matmul(x, self.W) + self.bias)
