import unittest
import numpy as np
from gates import Rz, Ry, H
from qiskit import Aer, execute, QuantumCircuit

from lab2 import rzryrz
from lab2 import operador_controlado
from lab2 import toffoli
from lab2 import inicializa_3qubits
from lab2 import inicializa

class test_lab2(unittest.TestCase):
    def test1(self):
        x = rzryrz(H)
        Hcalc = np.e**(x[0]*1j) * Rz(x[1]) @ Ry(x[2]) @ Rz(x[3])
        
        self.assertTrue(np.allclose(H, Hcalc))

    def test2(self):
        circuito2 = QuantumCircuit(2)
        circuito2.x(0)
        circuito2.append(operador_controlado(H), [0,1])

        backend = Aer.get_backend('statevector_simulator')
        job = execute(circuito2, backend)
        result = job.result()
        self.assertTrue(np.allclose(result.get_statevector(), [0, 1 / np.sqrt(2), 0, 1 / np.sqrt(2)]))

    def test3(self):
        circuito3 = QuantumCircuit(3)
        circuito3.x(0)
        circuito3.x(1)
        circuito3.append(toffoli(), [0, 1, 2])
        circuito3.measure_all()

        backend = Aer.get_backend('qasm_simulator')
        job = execute(circuito3, backend)
        result = job.result()
        self.assertTrue(result.get_counts()['111'] == 1024)
        

        circuito3 = QuantumCircuit(3)
        circuito3.x(0)
        circuito3.append(toffoli(), [0, 1, 2])
        circuito3.measure_all()

        backend = Aer.get_backend('qasm_simulator')
        job = execute(circuito3, backend)
        result = job.result()
        self.assertTrue(result.get_counts()['001'] == 1024)


        circuito3 = QuantumCircuit(3)
        circuito3.x(1)
        circuito3.append(toffoli(), [0, 1, 2])
        circuito3.measure_all()

        backend = Aer.get_backend('qasm_simulator')
        job = execute(circuito3, backend)
        result = job.result()
        self.assertTrue(result.get_counts()['010'] == 1024)
        

        circuito3 = QuantumCircuit(3)
        circuito3.append(toffoli(), [0, 1, 2])
        circuito3.measure_all()

        backend = Aer.get_backend('qasm_simulator')
        job = execute(circuito3, backend)
        result = job.result()
        self.assertTrue(result.get_counts()['000'] == 1024)

    def test4(self):
        state = np.array([np.sqrt(0.03), np.sqrt(0.07), np.sqrt(0.15), np.sqrt(0.05), np.sqrt(0.1), np.sqrt(0.3), np.sqrt(0.2), np.sqrt(0.1)], dtype="float")
        state = state/np.linalg.norm(state)
        circuito4 = inicializa_3qubits(state)
        backend = Aer.get_backend('statevector_simulator')
        job = execute(circuito4, backend)
        result = job.result()
        self.assertTrue(np.allclose(result.get_statevector(), state))

    def test5(self):
        state = np.array([np.sqrt(0.03), np.sqrt(0.07), np.sqrt(0.15), np.sqrt(0.05), np.sqrt(0.1), np.sqrt(0.3), np.sqrt(0.2), np.sqrt(0.1)], dtype="float")
        state = state/np.linalg.norm(state)
        circuito5 = inicializa(state)
        backend = Aer.get_backend('statevector_simulator')
        job = execute(circuito5, backend)
        result = job.result()
        self.assertTrue(np.allclose(result.get_statevector(), state))
