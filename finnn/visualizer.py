"""
FINNN - Visualizzatore 3D dell'icosaedro con attivazioni
"""

import sys
from pathlib import Path

try:
    current_dir = Path(__file__).parent
except NameError:
    current_dir = Path.cwd()

parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

import numpy as np
import torch
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from novabene.graph import vertices


class FINNNVisualizer:
    def __init__(self, neuron):
        self.neuron = neuron
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')

    def plot(self, input_vector=None, title="FINNN - Neurone Icosaedrico Attivo"):
        if input_vector is None:
            input_vector = torch.randn(1, 52, dtype=torch.float32)
        elif not torch.is_tensor(input_vector):
            input_vector = torch.from_numpy(np.array(input_vector, dtype=np.float32)).unsqueeze(0)

        with torch.no_grad():
            state = self.neuron.forward(input_vector)

        activations = state.view(1, 13, 4).abs().mean(dim=2).squeeze(0).numpy()
        centers = np.vstack([np.zeros(3), vertices])
        colors = plt.cm.plasma(activations / activations.max())

        self.ax.clear()
        self.ax.scatter(centers[:,0], centers[:,1], centers[:,2],
                        c=colors, s=180, edgecolor='black', linewidth=0.8)

        for i in range(12):
            self.ax.plot([0, centers[i+1,0]], [0, centers[i+1,1]], [0, centers[i+1,2]],
                         'gray', alpha=0.4, linewidth=1.2)

        self.ax.set_title(title, fontsize=15, pad=20)
        self.ax.set_xlabel('X'); self.ax.set_ylabel('Y'); self.ax.set_zlabel('Z')
        self.ax.view_init(elev=25, azim=45)
        plt.show()
