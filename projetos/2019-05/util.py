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

def get_results(circ, output, backend=None, shots=1024, circ_name='CIRCUIT'):
    """Shows the results given by the _circuit"""

    if backend is None:
        backend = Aer.get_backend('qasm_simulator')

    print("RESULT: ", end='')

    clsbits = ClassicalRegister(len(output))
    circ.add_register(clsbits)
    circ.measure(output, clsbits)
    circ.draw(scale=1.0, filename=circ_name)
    job_sim = execute(experiments=circ, backend=backend, shots=shots)

    result = job_sim.result()

    count = result.get_counts(circ)

    qub_chance = []
   
   
    for qub, cou in zip(count.keys(), count.values()):
        chance = (cou / shots) * 100
    
        print("|{}> -> {:.2f}%".format(qub, chance), end='\t')

        count[qub] = '{:.2f}%'.format(chance)

    return count