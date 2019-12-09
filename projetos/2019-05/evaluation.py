## matplotlib to see the circuits
# matplotlib inline
## qiskit standart
from qiskit import *
import numpy as np
from random import randint
import sys
from util import get_possible_inputs
from itertools import combinations

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

def init_inputs(circuit, qWI, inputs):
  """
    circuit: circuit that must be used to the function
    qWI: list qubits input
    inputs: list with position qubits must start with 1

    This function set up the initial state of the qubits
  """
  for i in range(len(inputs)):
      if inputs[i] == 1:
          circuit.x(qWI[i])

def feed_foward(circuit, weights, inputs, outputs, possible_combinations):
  """
    circuit: circuit that must be used to the function
    weights: qubits must be used to construct and multiply by inputs
    inputs: qubits must be used to construct and multiply by weights
    outputs: qubits where the output of each run will be saved
    possible_combinations: list with all the combinations of possible entries qubits states
  """
  count = 0
  if len(inputs) == 3:
    circuit.x(weights)
    for i in possible_combinations:
      """ step foward """
      init_inputs(circuit, inputs, i)
      circuit.barrier()
      multiply_input_weights(circuit, inputs, weights[0:len(i)])
      circuit.barrier()
      multiply_input_weights(circuit, inputs, weights[len(i):len(i)*2])
      circuit.barrier()
     
      majority(circuit, len(i), weights[0:len(i)], weights[len(i)*2])
      circuit.barrier()
      majority(circuit, len(i), weights[len(i): len(i)*2], weights[len(i)*2 + 1])
      circuit.barrier()
      majority(circuit, len(i)-1, weights[len(i)*2:], outputs)
      """ ------ """

      """ step foward reverse to reuse the weights on next iteration"""
      circuit.barrier()
      majority(circuit, len(i), weights[len(i): len(i)*2], weights[len(i)*2 + 1])
      circuit.barrier()
      majority(circuit, len(i), weights[0:len(i)], weights[len(i)*2])
      circuit.barrier()
      multiply_input_weights(circuit, inputs, weights[len(i):len(i)*2])
      circuit.barrier()
      multiply_input_weights(circuit, inputs, weights[0:len(i)])
      circuit.barrier()
      init_inputs(circuit, inputs, i)
      circuit.barrier()
      """ ------ """

      count+=1
    circuit.x(weights)
  else:
    """ Raise exception implementation """
    raise NotImplementedError
def load_data(data, q_inputs, q_output, circuit):
  """
   Loads the data in a quantum circuit with the inputs in superposition
   data: the data must follow the format [inputs, output], where output is the expected value
   q_inputs: the quantum register where are the inputs in superposition
   q_output: the quantum register that must load the expected value
   circuit: the quantum circuit used to load the data.
   returns: a quantum circuit with the data loaded.
  """
  for row in data:
      if row[-1] is 1:
          indexes = [i for i, e in enumerate(row[:-1]) if e == 1]
          if len(indexes) is 1:
              circuit.cx(indexes, q_output)
          elif len(indexes) is 2:
              circuit.ccx(indexes, q_output)
          else:
              for tup in combinations(indexes, 2):
                  circuit.ccx(tup, q_output)
  return circuit
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

    # Supondo que os valores iniciais são |0>
    qW = QuantumRegister(8, name='weights') 
    qI = QuantumRegister(3, name='inputs')
    c = ClassicalRegister(3)
    qO = QuantumRegister(1, name='output')
    # Construindo o circuito
    circuit = QuantumCircuit(qW, c)
    load_circuit = QuantumCircuit(qI, qO)

    load_circuit.h(qI)
    load_circuit = load_data(prob_1, qI, qO, load_circuit)

   
    circuit += load_circuit

    possible_inputs = get_possible_inputs(3)
    feed_foward(circuit, qW, qI, qO, possible_inputs)

    unload_circuit = QuantumCircuit(qI, qO)
    unload_circuit = load_data(prob_1, qI, qO, unload_circuit)
    
    unload_circuit.h(qI)
    circuit += unload_circuit
    
    # -----------------------------------------
    # Ver o circuit desenhado
    circuit.draw(output="mpl")
    circuit.measure(qI, c)
    job = qiskit.execute(circuit, backend)
    result = job.result()
    counts = result.get_counts(circuit)
    print(counts)


if __name__ == "__main__":
    main()
