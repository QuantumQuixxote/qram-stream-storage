from qiskit.circuit.instruction import Instruction
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.quantumregister import QuantumRegister
from qiskit.quantum_info import Statevector
import numpy as np
class QRAM:

    def __init__(self, n_address_bits, n_memory_cell_bits, stored_numbers):
        self._n_address_bits = n_address_bits
        self._n_memory_cell_bits = n_memory_cell_bits
        self._stored_numbers = stored_numbers

        # This architecture will store 2^n_address_bits items, each comprising of n_memory_cell_bits bits. 
        # Number of qubits needed:
        # Address - n_address_bits
        # Trigger - 2^n_address_bits
        # Memory - n_memory_cell_bits * 2^n_address_bits
        # Fanout - n_memory_cell_bits
        self.n_trigger_bits = 2**n_address_bits
        self._n_qubits = n_address_bits + self.n_trigger_bits + self.n_trigger_bits * n_memory_cell_bits + n_memory_cell_bits

        # List of qubits containing data
        self._memory_qubits = [i for i in range(n_address_bits + self.n_trigger_bits, n_address_bits + self.n_trigger_bits + self.n_trigger_bits * n_memory_cell_bits )]

        # Creation of the quantum circuit
        self._q = QuantumRegister(self._n_qubits)
        self._qc = QuantumCircuit(self._q, name="QRAM")

        for i in range(n_address_bits):
            for j in range(2**i):
                self._qc.ccx(i, n_address_bits + j, n_address_bits + j + 2**i)
            for j in range(2**i):
                self._qc.cx(n_address_bits + j + 2**i, n_address_bits + j)

        for i in range(self.n_trigger_bits):
            for j in range(n_memory_cell_bits):
                self._qc.ccx(n_address_bits + i, n_address_bits + self.n_trigger_bits + i*n_memory_cell_bits + j, n_address_bits + self.n_trigger_bits +  self.n_trigger_bits * n_memory_cell_bits + j)

        self.display()

    def _initialize_memory_cells(self) -> None:
        if len(self._stored_numbers) > 2 ** self._n_address_bits:
            print("Not enough storage qubits, please enter a shorter vector")
            return
        # initial_qc = QuantumCircuit(self._n_qubits)
        # Initialize each memory cell with exactly 1 number, using a one-hot encoding statevector
        for i, number in enumerate(self._stored_numbers):
            if number > 2 ** self._n_memory_cell_bits:
                print("Number too large: " + str(number), + ", please enter a smaller one.")
            else: 
                initial_sv = np.zeros(shape=2**self._n_memory_cell_bits)
                initial_sv[number] = 1
                # Initialize 1st number on 0 -> m-1 bits, 2nd number on m -> 2m - 1 bits, etc.
                self._qc.initialize(initial_sv, self._memory_qubits[i*self._n_memory_cell_bits:(i+1)*self._n_memory_cell_bits])
        # self._qc = initial_qc + self._qc
 
    def display(self) -> None:
        print(self._qc)

    def get_instruction(self) -> Instruction:
        print(self._qc)
        return self._qc.to_instruction()

    def get_inverse_instruction(self) -> Instruction:
        print(self._qc.inverse())
        return self._qc.inverse().to_instruction()
