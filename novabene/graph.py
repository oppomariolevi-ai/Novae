"""
Novae-Graph – Discrete Dirac Quantum Walk on Icosahedral Graph
Autore: Filippo Mario Oppo
"""

import sys
from pathlib import Path

# Fix robusto: funziona sia su Colab/Jupyter che da terminale
try:
    current_dir = Path(__file__).parent
except NameError:
    current_dir = Path.cwd()

if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

import numpy as np
from scipy.linalg import eigh

# Import da arithmetic.py (stessa cartella novabene/)
from arithmetic import (
    Nit, nit_add, nit_mul, nit_from_string, nit_to_string,
    SYMBOLS, _SYM_TO_DEC, _dec_to_nit
)

# === SETUP GEOMETRIA ICOSAEDRICA ===
phi = (1 + np.sqrt(5)) / 2
raw_vertices = np.array([
    [0, 1, phi], [0, 1, -phi], [0, -1, phi], [0, -1, -phi],
    [1, phi, 0], [1, -phi, 0], [-1, phi, 0], [-1, -phi, 0],
    [phi, 0, 1], [phi, 0, -1], [-phi, 0, 1], [-phi, 0, -1]
])

norm_factor = np.linalg.norm(raw_vertices[0])
vertices = raw_vertices / norm_factor * 2.0
center = np.array([0.0, 0.0, 0.0])

# Matrice di adiacenza
adj = np.zeros((12, 12), dtype=int)
a_theory = 2.0 * 4.0 / np.sqrt(10 + 2 * np.sqrt(5))
for i in range(12):
    for j in range(i + 1, 12):
        dist = np.linalg.norm(vertices[i] - vertices[j])
        if abs(dist - a_theory) < 1e-6:
            adj[i, j] = adj[j, i] = 1

# === Matrici Dirac ===
sigma1 = np.array([[0, 1], [1, 0]])
sigma2 = np.array([[0, -1j], [1j, 0]])
sigma3 = np.array([[1, 0], [0, -1]])
gamma0 = np.diag([1, 1, -1, -1])
gamma1 = np.block([[np.zeros((2, 2)), sigma1], [-sigma1, np.zeros((2, 2))]])
gamma2 = np.block([[np.zeros((2, 2)), sigma2], [-sigma2, np.zeros((2, 2))]])
gamma3 = np.block([[np.zeros((2, 2)), sigma3], [-sigma3, np.zeros((2, 2))]])
gamma = [gamma1, gamma2, gamma3]

def build_hamiltonian(g_coupling=1.0, mass_center=0.0):
    N_nodes, N_spin = 13, 4
    dim = N_nodes * N_spin
    H = np.zeros((dim, dim), dtype=complex)

    # Centro → vertici
    for v in range(12):
        dx = vertices[v] - center
        dist = np.linalg.norm(dx)
        dx_hat = dx / dist
        gamma_proj = sum(gamma[m] * dx_hat[m] for m in range(3))
        for a in range(4):
            for b in range(4):
                idx_c = 0 * 4 + a
                idx_v = (v + 1) * 4 + b
                val = -1j * (g_coupling / dist) * gamma_proj[a, b]
                H[idx_c, idx_v] += val
                H[idx_v, idx_c] += np.conjugate(val)

    # Vertice ↔ vertice
    for i in range(12):
        for j in range(12):
            if adj[i, j] and i < j:
                dx = vertices[j] - vertices[i]
                dist = np.linalg.norm(dx)
                dx_hat = dx / dist
                gamma_proj = sum(gamma[m] * dx_hat[m] for m in range(3))
                for a in range(4):
                    for b in range(4):
                        idx_i = (i + 1) * 4 + a
                        idx_j = (j + 1) * 4 + b
                        val = -1j * (1.0 / dist) * gamma_proj[a, b]
                        H[idx_i, idx_j] += val
                        H[idx_j, idx_i] += np.conjugate(val)

    if mass_center != 0.0:
        for a in range(4):
            for b in range(4):
                idx = 0 * 4 + a
                H[idx, idx] += mass_center * gamma0[a, b]

    return H

# === TEST + GRAFICI ===
if __name__ == "__main__":
    lambda_val = 0.5
    print("Test scaling lineare (Novae-Graph):")
    for n in [1, 10, 100, 1000]:
        H = build_hamiltonian(mass_center=lambda_val * n)
        eigvals = eigh(H)[0]
        E_gs = np.min(np.abs(eigvals[eigvals > 0]))
        print(f"n={n:4d} → E_gs={E_gs:.5f}  |E|/n={E_gs/n:.5f}")

    H_test = build_hamiltonian(mass_center=lambda_val * 1)
    error = np.linalg.norm(H_test - H_test.conj().T)
    print(f"\nErrore hermitiana: {error:.2e} (deve essere ~0)")

    # Grafici
    import matplotlib.pyplot as plt
    ns = [1, 10, 50, 100, 500, 1000]
    Egs_list = []
    for n in ns:
        H = build_hamiltonian(mass_center=0.5 * n)
        eigvals = eigh(H)[0]
        Egs = np.min(np.abs(eigvals[eigvals > 0]))
        Egs_list.append(Egs)

    plt.figure(figsize=(8, 5))
    plt.plot(ns, Egs_list, 'o-', linewidth=2, markersize=8, label='E_ground-state')
    plt.plot(ns, [0.5 * n for n in ns], '--', label='Riferimento lineare E = λ·n (λ=0.5)')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Numero combinatorio n_tot')
    plt.ylabel('Energia ground-state')
    plt.title('Novae-Graph: Scaling dell’energia (Dirac discreto)')
    plt.legend()
    plt.grid(True, which='both')
    plt.savefig('energy_scaling.png', dpi=200, bbox_inches='tight')
    print("✅ Salvato: energy_scaling.png")

    H1 = build_hamiltonian(mass_center=0.5 * 1)
    eigvals1 = np.sort(eigh(H1)[0])
    plt.figure(figsize=(8, 5))
    plt.plot(eigvals1, 'o', markersize=4)
    plt.axhline(0, color='red', linestyle='--', linewidth=1)
    plt.title('Spettro completo della Hamiltoniana (n=1) – 52 autovalori')
    plt.xlabel('Indice autovalore')
    plt.ylabel('Energia')
    plt.grid(True)
    plt.savefig('spectrum_n1.png', dpi=200, bbox_inches='tight')
    print("✅ Salvato: spectrum_n1.png")
