## matplotlib to see the circuits
# matplotlib inline
## qiskit standart
from qiskit import *
import numpy as np
from random import randint
import sys

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
    print("Not implemented yet!")

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
      majority(circuit, len(i)-1, weights[len(i)*2:], outputs[count])
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

def main():
    # Supondo que os valores iniciais são |0>
    qWI = QuantumRegister(7) 
    c = ClassicalRegister(1)
    outputs = QuantumRegister(8)
    # Construindo o circuito
    circuit = QuantumCircuit(qWI, c)
    # definindo a quantidade de inputs
    qtd_input = 3

    circuit.x(qWI[0])
    circuit.x(qWI[2])
    # Então, aqui temos a implementação de um perceptron com 3 entradas.
    circuit.x(qWI[3:6])
    multiply_input_weights(circuit, qWI[0:3], qWI[3:])
    circuit.x(qWI[3:6])

    majority(circuit, qtd_input, qWI[3:6], qWI[6])
    circuit.measure(qWI[6], c[0])

    feed_foward(circuit, qWI[3:6], qWI[0:3], outputs)

    # -----------------------------------------
    # Ver o circuit desenhado
    circuit.draw(output="mpl")
    
    job = qiskit.execute(circuit, backend,)
    result = job.result()
    counts = result.get_counts(circuit)
    print(counts)


if __name__ == "__main__":
    main()
