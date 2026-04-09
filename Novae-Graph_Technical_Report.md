# Novae-Graph  
**Discrete Dirac Quantum Walk on the Icosahedral Lattice**

**Technical Report**  
Filippo Mario Oppo – Perito Elettrotecnico  
Roma, Aprile 2026  

## Abstract
Novae-Graph è un’implementazione numerica efficiente di dinamica Dirac discreta su un grafo icosaedrico a 13 nodi (kissing number 3D).  
Viene costruita una Hamiltoniana hermitiana 52×52 e viene dimostrato numericamente lo scaling dell’energia ground-state con il numero combinatorio n_tot.  
Il framework è **pronto per prototipazione FPGA** e costituisce una base concreta per simulazioni quantistiche discrete, modellazione di nanostrutture e ricerca in quantum computing applicato.

## 1. Framework geometrico
Il grafo deriva dal massimo impacchettamento di sfere in 3D (kissing number = 12).  
13 nodi totali (12 vertici + centro), ciascuno dotato di uno spinore Dirac a 4 componenti.  
Distanza centro-vertici normalizzata a 2 unità (unità naturali ħ = c = 1).

## 2. Costruzione della Hamiltoniana
H = H_kin + H_mass  
- H_kin: termini di hopping tra nodi adiacenti tramite matrici γμ di Dirac  
- H_mass: concentrato al centro (m = λ · n_tot, λ = 0.5)

La matrice 52×52 è **hermitiana** (errore Frobenius = 0.00e+00) e soddisfa l’algebra di Clifford.

## 3. Risultati numerici (verificato con SciPy)

![Scaling energia](energy_scaling.png)  
*Scaling dell’energia ground-state al variare di n_tot. Si osserva transizione da regime quasi-lineare a saturazione (localizzazione al centro).*

![Spettro Hamiltoniana](spectrum_n1.png)  
*Spettro completo dei 52 autovalori per n_tot = 1. Simmetria particella-antiparticella perfetta.*

**Osservazioni chiave**:
- Per piccoli n_tot l’energia scala quasi linearmente  
- Per n_tot ≫ 1 si ha saturazione → fenomeno fisico di localizzazione  
- Spettro simmetrico e numericamente stabile

## 4. Rilevanza industriale e competenze dimostrate
Questo progetto dimostra in modo concreto:
- Padronanza di algebra lineare numerica e meccanica quantistica discreta  
- Sviluppo di codice scientifico efficiente (NumPy + SciPy)  
- Approccio hardware-oriented (modello pronto per implementazione FPGA)  
- Capacità di trasformare un’idea teorica in un prototipo verificabile

**Applicazioni dirette**:
- Simulazione di nanostrutture icosaedriche (fullerene, virus, quasicristalli)  
- Prototipazione di algoritmi quantum-walk per ottimizzazione combinatoria  
- Base per sistemi embedded di prossima generazione in aerospace e difesa

## 5. Sviluppi futuri (in corso)
- Implementazione FPGA dell’addizione signed-digit a 21 stati (core Novabene)  
- Quantum walk temporale con operatore split-step unitary  
- Estensione a grafi multi-livello per modellazione atomica discreta

**Codice completo**: `novabene_graph.py` (repo Novae)  
**Licenza**: MIT

---

**Filippo Mario Oppo**  
Perito Elettrotecnico | FPGA & Discrete Physics Innovator  
Roma, Lazio | Disponibile da subito per ruoli R&D embedded, prototipazione hardware e quantum computing applicato.
