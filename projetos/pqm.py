'''
PQM class for probabilistic quantum memories
'''

# pylint: disable=no-member

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, BasicAer, execute
import math as sp


class PQM:
    ''' Simulation of a probabilistic quantum memory based
        on arXiv:quant-ph/0204115
    '''

    def __init__(self, size):
        '''
            Creates a probabilistic quantum memory
            size: Number of qbits used in the memory
        '''
        self._memory = QuantumRegister(size, 'm')
        self._ancillary = QuantumRegister(1, 'c')
        self._bit = ClassicalRegister(1, 'bit')
        self._size = size
        self._circuit = QuantumCircuit(self._memory, self._ancillary, self._bit)

    def load_data(self, data=None):
        ''' memory initialization'''

        params = (2 ** self._size) * [0]

        if data is None:
            params[0] = 1
        else:
            number_patterns = len(data)
            amplitude = 1.0 / sp.sqrt(number_patterns)

            for pattern in data:
                index = self._bin_pattern_to_number(pattern)
                params[index] = amplitude

        self._circuit.initialize(params, self._memory)

    def recover(self, input_pattern=None, t=0.044):
        '''
        :param t: Parametric Value
        :param input_pattern: (size,) array of 0s and 1s
                              input pattern for recovering algorithm
        :return circuit:      quantum circuit of PQM recovering algorithm
        '''

        if input_pattern is not None:
            for k, value in enumerate(input_pattern):
                if value == 1:
                    self._circuit.x(self._memory[k])
        for k in range(self._size):
            self._circuit.u1(sp.pi / (2 * self._size * t), self._memory[k])

        # initialize auxiliary quantum bit |c>
        self._circuit.h(self._ancillary[0])
        for k in range(self._size):
            self._circuit.cu1(- sp.pi / (self._size * t), self._ancillary[0], self._memory[k])
        self._circuit.h(self._ancillary[0])

        self._circuit.measure(self._ancillary[0], self._bit[0])

    def run(self, number_shots=1024, backend=BasicAer.get_backend('qasm_simulator')):
        '''
        :param backend: Backend to run the PQM
        :param number_shots: Number of repetitions
        :return: number of 0s and 1s after number_shots executions
        '''
        job = execute(self._circuit, backend, shots=number_shots)
        result = job.result()
        counts = result.get_counts(self._circuit)
        return counts

    @staticmethod
    def _bin_pattern_to_number(pattern):
        aindex = 0
        for i, value in enumerate(pattern):
            aindex += value * 2 ** i
        return aindex

    def __str__(self):
        str_circuit = self._circuit.draw()
        return str(str_circuit)


if __name__ == '__main__':
    mem_2 = [[1, 1, 1, 1, 0, 1, 0, 1, 1, 0], [1, 1, 0, 0, 0, 1, 0, 1, 0, 1], [1, 1, 0, 1, 0, 1, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 0, 0, 1, 0, 1]]
    mem_1 = [[0, 1, 1, 0, 0, 1, 0, 1, 0, 1], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1], [0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
             [0, 0, 1, 1, 0, 1, 0, 1, 0, 1]]

    pqm = PQM(len(mem_2[0]))
    print(pqm.__dict__)
    pqm.load_data(mem_2)
    pqm.recover([0, 1, 1, 1, 0, 1, 0, 1, 0, 1])
    out = pqm.run(8192)
    print(str(out['0'] * 100 / 8192) + '%')
    print(pqm)
