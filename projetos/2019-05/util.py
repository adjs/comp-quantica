from itertools import combinations, combinations_with_replacement, permutations, product
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute, IBMQ
from qiskit.providers.jobstatus import JOB_FINAL_STATES
import numpy as np
import time

def get_possible_inputs(size, positions=None):

    if positions is None:
        all_positions = generate_positions(size)

    """
        position: a array with position that might be one,
        size: The size of the binary array
        return: a array with binary values: 0, 1
    """
    array = []
    binary = [0] * size
    
    for tup in all_positions:
        for index in tup:
            binary[index] = 1
        binary = [0]*size
        array.append(binary)

    return array

def generate_positions(inputs_size):
    """Generate the inputs to the QBNN combining the positions of
       the quantum registers that can be changed to 1"""

    inputs = []
    regs = np.arange(inputs_size)
    for n_reg in range(inputs_size + 1):
        
        inputs.extend(list(combinations(regs, n_reg)))
    
    return inputs
