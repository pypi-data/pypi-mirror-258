# qsm

Module Python pour la manipulation de circuits quantiques.

## Installation

```bash
pip install qsm
```

## Example d Utilisation:

```python

from qsm import QuantumCircuit

# Créer un circuit quantique avec 3 qubits
circuit = QuantumCircuit(3)

# Appliquer une porte Hadamard sur le premier qubit
circuit.h(0)

# Appliquer une porte CNOT entre le premier et le deuxième qubit
circuit.cx(0, 1)

# Mesurer l'état du circuit
resultats = circuit.measure_all(shots=1024)
print(resultats)

```

### Licence

ce projet est sous licence particulier, juste un message au proprietaire du module pour son accord pour la copie, etc..

### Contribution

ce projet peut etre contribué par differente maniére:
    reddit laisser un message pour contribué dans r/python                             
    github créer un repertoire pour ajouter des fonctionnalité si neccéssaire

