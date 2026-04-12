import numpy as np
from scipy.linalg import eigh

try:
    from .arithmetic import Nit, _SYM_TO_DEC, _DEC_TO_SYM
except ImportError:
    from arithmetic import Nit, _SYM_TO_DEC, _DEC_TO_SYM

def _dec_to_nit(val): return _DEC_TO_SYM[val]

phi = (1 + np.sqrt(5)) / 2
raw_vertices = np.array([
    [0, 1, phi], [0, 1, -phi], [0, -1, phi], [0, -1, -phi],
    [1, phi, 0], [1, -phi, 0], [-1, phi, 0], [-1, -phi, 0],
    [phi, 0, 1], [phi, 0, -1], [-phi, 0, 1], [-phi, 0, -1]
])
norm_factor = np.linalg.norm(raw_vertices[0])
vertices = raw_vertices / norm_factor * 2.0
center = np.array([0.0, 0.0, 0.0])
adj = np.zeros((12, 12), dtype=int)
a_theory = 2.0 * 4.0 / np.sqrt(10 + 2 * np.sqrt(5))
for i in range(12):
    for j in range(i+1, 12):
        if abs(np.linalg.norm(vertices[i]-vertices[j]) - a_theory) < 1e-6:
            adj[i,j] = adj[j,i] = 1

sigma1 = np.array([[0,1],[1,0]])
sigma2 = np.array([[0,-1j],[1j,0]])
sigma3 = np.array([[1,0],[0,-1]])
gamma0 = np.diag([1,1,-1,-1])
gamma1 = np.block([[np.zeros((2,2)),sigma1],[-sigma1,np.zeros((2,2))]])
gamma2 = np.block([[np.zeros((2,2)),sigma2],[-sigma2,np.zeros((2,2))]])
gamma3 = np.block([[np.zeros((2,2)),sigma3],[-sigma3,np.zeros((2,2))]])
gamma = [gamma1, gamma2, gamma3]

def build_hamiltonian(g_coupling=1.0, mass_center=0.0):
    N_nodes, N_spin = 13, 4
    dim = N_nodes * N_spin
    H = np.zeros((dim, dim), dtype=complex)
    for v in range(12):
        dx = vertices[v] - center
        dist = np.linalg.norm(dx)
        dx_hat = dx / dist
        gamma_proj = sum(gamma[m] * dx_hat[m] for m in range(3))
        for a in range(4):
            for b in range(4):
                idx_c = 0*4 + a
                idx_v = (v+1)*4 + b
                val = -1j * (g_coupling / dist) * gamma_proj[a,b]
                H[idx_c, idx_v] += val
                H[idx_v, idx_c] += np.conjugate(val)
    for i in range(12):
        for j in range(12):
            if adj[i,j] and i<j:
                dx = vertices[j] - vertices[i]
                dist = np.linalg.norm(dx)
                dx_hat = dx / dist
                gamma_proj = sum(gamma[m] * dx_hat[m] for m in range(3))
                for a in range(4):
                    for b in range(4):
                        idx_i = (i+1)*4 + a
                        idx_j = (j+1)*4 + b
                        val = -1j * (1.0 / dist) * gamma_proj[a,b]
                        H[idx_i, idx_j] += val
                        H[idx_j, idx_i] += np.conjugate(val)
    if mass_center != 0.0:
        for a in range(4):
            for b in range(4):
                idx = 0*4 + a
                H[idx, idx] += mass_center * gamma0[a,b]
    return H
