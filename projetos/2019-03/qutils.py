from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, Aer, execute
import numpy as np
import math as m
import scipy as sci

S_simulator = Aer.backends(name='statevector_simulator')[0]
M_simulator = Aer.backends(name='qasm_simulator')[0]

def wavefunction(obj, *args, **kwargs):
	if(type(obj) == QuantumCircuit):
		statevec = execute(obj, S_simulator, shots=1).result().get_statevector()
	if(type(obj) == np.ndarray):
		statevec = obj
	sys = False
	NL = False
	dec = 5
	if 'precision' in kwargs:
		dec = int(kwargs['precision'])
	if 'column' in kwargs:
		NL = kwargs['column']
	if 'systems' in kwargs:
		systems = kwargs['systems']
		sys = True
		last_sys = int(len(systems)-1)
		show_systems = []
		for s_chk in np.arange(len(systems)):
			if(type(systems[s_chk]) != int):
				raise Exception('systems must be an array of all integers')
		if 'show_systems' in kwargs:
			show_systems = kwargs['show_systems']
			if(len(systems) != len(show_systems)):
				raise Exception('systems and show_systems need to be arrays of equal lenght')
			for ls in np.arange(len(show_systems)):
				if((show_systems[ls] != True) and (show_systems[ls] != False)):
					raise Exception('show_systems must be an array of Truth Values')
				if(show_systems[ls] == True):
					last_sys = int(ls)
		else:
			for ss in np.arange(len(systems)):
				show_systems.append(True)
	wf = ''
	qubits = int(m.log(len(statevec), 2))
	for i in np.arange(int(len(statevec))):
		value = round(statevec[i].real, dec) + round(statevec[i].imag, dec) * 1j
		if ((value.real != 0) or (value.imag != 0)):
			state = list(to_binary(int(i), int(2**qubits)))
			state_str = ''
			if (sys == True):
				k = 0
				for s in np.arange(len(systems)):
					if (show_systems[s] == True):
						if (int(s) != last_sys):
							state.insert(int(k + systems[s]), '>|')
							k = int(k + systems[s] + 1)
						else:
							k = int(k + systems[s])
					else:
						for s2 in np.arange(systems[s]):
							del state[int(k)]
			for j in np.arange(len(state)):
				if (type(state[j]) != str):
					state_str = state_str + str(int(state[j]))
				else:
					state_str = state_str + state[j]
			if ((value.real != 0) and (value.imag != 0)):
				if (value.imag > 0):
					wf = wf + str(value.real) + '+' + str(value.imag) + 'j |' + state_str + '>   '
				else:
					wf = wf + str(value.real) + '' + str(value.imag) + 'j |' + state_str + '>   '
				
			if ((value.real != 0) and (value.imag == 0)):
				state_str = state_str[::-1]
				wf = wf + str(value.real) + '  |' + state_str + '>   '
			if ((value.real == 0) and (value.imag != 0)):
				state_str = state_str[::-1]
				wf = wf + str(value.imag) + 'j  |' + state_str + '>   '
			if (NL):
				wf = wf + '\n'
	print(wf)
    
def to_binary(number, total):
    qubits = int(m.log(total, 2))
    N = number
    b_num = np.zeros(qubits)
    for i in np.arange(qubits):
        if (N/((2)**(qubits-i-1)) >= 1):
            b_num[i] = 1
            N = N - 2**(qubits-i-1)
    B = []
    for j in np.arange(len(b_num)):
        B.append(int(b_num[j]))
    return B

def measurement(quantumcircuit, *args, **kwargs):
    p_M = True
    S = 1
    ret = False
    NL = False
    if 'shots' in kwargs:
        S = int(kwargs['shots'])
    if 'return_M' in kwargs:
        ret = kwargs['return_M']
    if 'print_M' in kwargs:
        p_M = kwargs['print_M']
    if 'column' in kwargs:
        NL = kwargs['column']
    M1 = execute(quantumcircuit, M_simulator, shots = S).result().get_counts(quantumcircuit)
    M2 = {}
    k1 = list(M1.keys())
    v1 = list(M1.values())
    for k in np.arange(len(k1)):
        key_list = list(k1[k])
        new_key = ''
        for j in np.arange(len(key_list)):
            new_key = new_key + key_list[len(key_list) - (j + 1)]
        M2[new_key] = v1[k]
    if (p_M):
        k2 = list(M2.keys())
        v2 = list(M2.values())
        measurements = ''
        for i in np.arange(len(k2)):
            m_str = str(v2[i]) + ' |'
            for j in np.arange(len(k2[i])):
                if (k2[i][j] == '0'):
                    m_str = m_str + '0'
                if (k2[i][j] == '1'):
                    m_str = m_str + '1'
                if (k2[i][j] == ' '):
                    m_str = m_str + '>| '
            m_str = m_str + '>  '
            if (NL):
                m_str = m_str + '\n'
            measurements = measurements + m_str
        print(measurements)
    if (ret):
        return M2