import qiskit

def inicializa_estado_Bell(estado):
    circ = qiskit.QuantumCircuit(2)
    if estado == 1 or estado ==3:
        circ.x(1)
    if estado == 2 or estado == 3:
        circ.x(0)

    circ.h(1)
    circ.cx(1, 0)
    
    return circ
