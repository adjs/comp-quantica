import numpy as np
import qiskit

def Rz(theta):
    return np.array([[np.e**(-1j*theta/2), 0],[0, np.e**(1j*theta/2)]])

def Ry(theta):
    return np.array([[np.cos(theta/2), -np.sin(theta/2)],[np.sin(theta/2), np.cos(theta/2)]])

H = 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]])
