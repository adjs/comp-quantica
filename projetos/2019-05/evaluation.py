## matplotlib to see the circuits
# matplotlib inline
## qiskit standart
from qiskit import *
import numpy as np
from random import randint
import sys
from util import get_possible_inputs, get_results
from itertools import combinations
import json

if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")
## See available eviroments
Aer.backends()

backend = BasicAer.get_backend('qasm_simulator')


def multiply_input_weights(circuit, qWI_control, qWI_controled):
    """
    circuit: circuit that must be used to the function
    qWI_contol and qWI_controled: qubits wich will be used to mutiply eache other
  """
    for i in range(len(qWI_control)):
        circuit.cx(qWI_control[i], qWI_controled[i])


def majority(circuit, qtd, qWI, target):
    """
    circuit: circuit that must be used to the function
    qtd: quantity of qubits that we will build the function
    qWI: list with qubits that will be used to build the function majority
    target: qubit wich we will set the final result
  """
    if qtd == 2:
        circuit.ccx(qWI[0], qWI[1], target)
        circuit.cx(qWI[0], target)
        circuit.cx(qWI[1], target)
    elif qtd == 3:
        circuit.ccx(qWI[0], qWI[1], target)
        circuit.ccx(qWI[0], qWI[2], target)
        circuit.ccx(qWI[1], qWI[2], target)
    else:
        """ Raise exception implementation """
        raise NotImplementedError


def init_weights(circuit, qWI, inputs):
    """
    circuit: circuit that must be used to the function
    qWI: list qubits input
    inputs: list with position qubits must start with 1

    This function set up the initial state of the qubits
  """
    for i in range(len(inputs)):
        if inputs[i] == 1:
            circuit.x(qWI[i])


def feed_foward(circuit, weights, inputs, outputs, weights_combination, weight_size=3):
    """
    circuit: circuit that must be used to the function
    weights: qubits must be used to construct and multiply by inputs
    inputs: qubits must be used to construct and multiply by weights
    outputs: qubits where the output of each run will be saved
    possible_combinations: list with all the combinations of possible weights qubits states
  """
    dj_aux = QuantumRegister(1, name='dj_ancillary')
    circuit.add_register(dj_aux)
    circuit.x(dj_aux)
    circuit.h(dj_aux)

    init_weights(circuit, weights, weights_combination)  # Initialize a given weights combination

    count = 0
    if len(inputs) == 3:
        circuit.x(weights)

        """ step foward """
        circuit.barrier()
        multiply_input_weights(circuit, inputs, weights[0:weight_size])
        circuit.barrier()
        multiply_input_weights(circuit, inputs, weights[weight_size:weight_size * 2])
        circuit.barrier()

        majority(circuit, weight_size, weights[0:weight_size], weights[weight_size * 2])
        circuit.barrier()
        majority(circuit, weight_size, weights[weight_size: weight_size * 2], weights[weight_size * 2 + 1])
        circuit.barrier()
        majority(circuit, weight_size - 1, weights[weight_size * 2:], outputs)
        """ ------
    Evaluation
    """
        circuit.cx(outputs, dj_aux)

        """ step foward reverse to reuse the weights on next iteration"""
        circuit.barrier()
        majority(circuit, weight_size - 1, weights[weight_size * 2:], outputs)
        circuit.barrier()
        majority(circuit, weight_size, weights[weight_size: weight_size * 2], weights[weight_size * 2 + 1])
        circuit.barrier()
        majority(circuit, weight_size, weights[0:weight_size], weights[weight_size * 2])
        circuit.barrier()
        multiply_input_weights(circuit, inputs, weights[weight_size:weight_size * 2])
        circuit.barrier()
        multiply_input_weights(circuit, inputs, weights[0:weight_size])
        circuit.barrier()
        init_weights(circuit, weights, weights_combination)
        circuit.barrier()
        """ ------ """

        count += 1
        circuit.x(weights)
    else:
        """ Raise exception implementation """
        raise NotImplementedError


def load_data(data, q_inputs, q_output, unload=False):
    """
   Loads the data in a quantum circuit with the inputs in superposition
   data: the data must follow the format [inputs, output], where output is the expected value
   q_inputs: the quantum register where are the inputs in superposition
   q_output: the quantum register that must load the expected value
   circuit: the quantum circuit used to load the data.
   unload: Decides if the data must be or not unloaded
   returns: a quantum circuit with the data loaded.
  """
    aux = QuantumRegister(1, name='mct_ancillary')
    load_circuit = QuantumCircuit(q_inputs, q_output, aux)

    if not unload:
        load_circuit.h(q_inputs)

    for row in data:
        if row[-1] is 1:
            indexes_0 = [i for i, e in enumerate(row[:-1]) if e == 0]

            load_circuit.x(indexes_0)
            load_circuit.mct(q_inputs, q_output[0], aux)
            load_circuit.x(indexes_0)

    if unload:
        load_circuit.h(q_inputs)

    return load_circuit


def run_experiment(problem, name='Experiment'):
    experiments = {'problem': name}
    trial = 0
    for combination in get_possible_inputs(8):
        trial += 1

        print('Trial ', trial, end='')
        print('-' * 50)
        print('Testing weights: ', combination)

        # Initializing the registers with |0>
        qW = QuantumRegister(8, name='weights')
        qI = QuantumRegister(3, name='inputs')
        qO = QuantumRegister(1, name='output')

        # Building the circuit
        circuit = QuantumCircuit(qW, qI, qO)

        # Loading the data
        load_circuit = load_data(problem, qI, qO)
        circuit += load_circuit

        feed_foward(circuit, qW, qI, qO, combination)

        unload_circuit = load_data(problem, qI, qO, True)

        # Unload the data
        circuit += unload_circuit
        circuit.barrier()
        result = get_results(circuit, qI, shots=1024)

        result['weights'] = combination

        experiments[trial] = {'outcomes': result}
        print()
        print('-' * 50)

    file_name = '_'.join(name).lower()
    with open(file_name + '.json', 'w', encoding='utf-8') as f:
        json.dump(experiments, f, ensure_ascii=False, indent=4)

    # -----------------------------------------


def main():
    prob_1 = [
        [0, 0, 0, 0],
        [0, 0, 1, 1],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 1, 0],
        [1, 1, 0, 0],
        [1, 1, 1, 0]
    ]

    prob_2 = [
        [0, 0, 0, 1],
        [0, 0, 1, 1],
        [0, 1, 0, 1],
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 1, 0],
        [1, 1, 0, 0],
        [1, 1, 1, 0]
    ]

    run_experiment(prob_2)


if __name__ == "__main__":
    main()
