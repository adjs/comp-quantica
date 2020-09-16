import numpy as np

def Rz(theta):
    return np.array([[np.e**(-1j*theta/2), 0],[0, np.e**(1j*theta/2)]])

def Ry(theta):
    return np.array([[np.cos(theta/2), -np.sin(theta/2)],[np.sin(theta/2), np.cos(theta/2)]])
