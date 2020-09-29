import qiskit
import numpy as np

def rzryrz(U):
    '''
    Lab2 - questão 1
    :param U: matriz unitária 2 x 2
    :return: [alpha, beta, gamma e delta]
            U = e^(1j * alpha) * Rz(beta) * Ry(gamma) * Rz(delta)
    '''

    # -----------------
    # Seu código aqui

    alpha = 0
    beta = 0
    gamma = 0
    delta = 0
    # -----------------

    return [alpha, beta, gamma, delta]

def operador_controlado(V):
    '''
    Lab2 - questão 2
    :param V: matriz unitária 2 x 2
    :return: circuito quântico com dois qubits aplicando o
             o operador V controlado.
    '''

    circuito = qiskit.QuantumCircuit(2)

    #-----------------
    # Seu código aqui
    # -----------------

    return circuito


def toffoli():
    '''
    Lab2 - questão 3
    :param n: número de controles
    :param V:
    :return: circuito quântico com n+1 qubits + n-1 qubits auxiliares
            que aplica o operador nCV.
    '''
    controles = qiskit.QuantumRegister(2)
    alvo = qiskit.QuantumRegister(1)



    circuito = qiskit.QuantumCircuit(controles, alvo)

    #------------------------
    # Seu código aqui
    # ------------------------

    return circuito

def inicializa_3qubits(vetor_dimensao8):
    '''
    Lab2 - questão 4
    '''

    circuito = qiskit.QuantumCircuit(3)

    # ------------------------
    # Seu código aqui
    # ------------------------

    return circuito

def inicializa(vetor):
    '''
    Lab2 - questão 5 - opcional
    '''
    circuito = qiskit.QuantumCircuit()

    return circuito
