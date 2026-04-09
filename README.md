# Novae (ex Novabene)

**Un framework geometrico-discreto per fisica, matematica e computing**

Sistema numerico a 21 stati bilanciati + dinamica Dirac discreta su grafo icosaedrico (kissing number 12).

- **Autore**: Filippo Mario Oppo (Perito Elettrotecnico)
- **Scopo**: Dimostrare competenze in **aritmetica non-standard**, **hardware modulare** e **simulazione quantistica discreta**
- **Tecnologie**: Python, NumPy, SciPy, pronto per FPGA

## 📌 Cosa contiene

### 1. Sistema numerico a 21 simboli (Novabene core)
- 21 stati: ∅, +0, −0, ±1…±9
- Addizione **signed-digit** con riporto locale massimo ±1 (non fully carry-free, ma con propagazione limitata e parallela su tutte le cifre)
- Tre zeri distinti con semantica fisica (vuoto / particella / antiparticella)

### 2. Novae-Graph: Discrete Dirac Quantum Walk
- Grafo icosaedrico 13 nodi (12 vertici + centro)
- Hamiltoniana Dirac 52×52 hermitiana e unitaria
- Simulazione di scaling dell’energia con numero combinatorio `n_tot`
- Codice verificato e pronto per prototipazione FPGA

## 🚀 Demo (esegui localmente)

```bash
pip install numpy scipy
python novabene_graph.py
