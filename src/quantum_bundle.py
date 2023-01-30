import os
from dotenv import load_dotenv

load_dotenv()


from azure.quantum import Workspace


workspace = Workspace (
    subscription_id = os.getenv("QUANTUM_SUBSCRIPTION_ID"), 
    resource_group = os.getenv("QUANTUM_RESOURCE_GROUP"),   
    name = os.getenv("QUANTUM_NAME"),          
    location = os.getenv("QUANTUM_LOCATION")        
    )

from qiskit import QuantumCircuit, transpile, assemble
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
from azure.quantum.qiskit import AzureQuantumProvider

provider = AzureQuantumProvider(
  resource_id=os.getenv("QUANTUM_RESOURCE_ID"),
  location=os.getenv("QUANTUM_LOCATION")
)





def initialize_s(qc, qubits):
    """Apply a H-gate to 'qubits' in qc"""
    for q in qubits:
        qc.h(q)
    return qc

def compute_result(items):

	n = 3
	qc = QuantumCircuit(n)

	position = select_item(items)

	qc = implement_circuit(qc, position)

	print("POSITION!!!")
	print(position)

	oracle_ex3 = qc.to_gate()
	oracle_ex3.name = "Oracle"


	def diffuser(nqubits):
	    qc = QuantumCircuit(nqubits)
	    # Apply transformation |s> -> |00..0> (H-gates)
	    for qubit in range(nqubits):
	        qc.h(qubit)
	    # Apply transformation |00..0> -> |11..1> (X-gates)
	    for qubit in range(nqubits):
	        qc.x(qubit)
	    # Do multi-controlled-Z gate
	    qc.h(nqubits-1)
	    qc.mct(list(range(nqubits-1)), nqubits-1)  # multi-controlled-toffoli
	    qc.h(nqubits-1)
	    # Apply transformation |11..1> -> |00..0>
	    for qubit in range(nqubits):
	        qc.x(qubit)
	    # Apply transformation |00..0> -> |s>
	    for qubit in range(nqubits):
	        qc.h(qubit)
	    # We will return the diffuser as a gate
	    U_s = qc.to_gate()
	    U_s.name = "Diffuser Function"
	    return U_s


	n = 3
	grover_circuit = QuantumCircuit(n)
	grover_circuit = initialize_s(grover_circuit, [0,1,2])
	grover_circuit.append(oracle_ex3, [0,1,2])
	grover_circuit.append(diffuser(n), [0,1,2])
	grover_circuit.measure_all()
	print(grover_circuit.draw())


	simulator_backend = provider.get_backend("ionq.simulator")


	transpiled_grover_circuit = transpile(grover_circuit, simulator_backend)
	qobj = assemble(transpiled_grover_circuit)



	# Submit the circuit to run on Azure Quantum
	job = simulator_backend.run(qobj, shots=100)
	job_id = job.id()
	print("Job id", job_id)

	# Monitor job progress and wait until complete:
	job_monitor(job)

	result = job.result()
	print("result below!!")
	# print(result)
	# print(result.get_counts())

	result_dict = result.get_counts()

	index_ = int(list(result_dict.keys())[0], 2) + int(list(result_dict.keys())[1], 2) - 9

	return items[index_]['id']




def select_item(items_list):
	for i in range(len(items_list)):
		print("ITEM LOOP!!!!!!!")
		print(items_list[i])
		if items_list[i]["label"] == "drug":
			return i
		if i >= 5:
			break
	return None

def implement_circuit(qc, n_position):
	if n_position == 0:
		qc.cz(0, 1)
		qc.cz(1, 2)
	if n_position == 1:
		qc.cz(0, 1)
	if n_position == 2:
		qc.cz(0, 2)
		qc.cz(1, 2)
	if n_position == 3:
		qc.cz(0, 2)
	if n_position == 4:
		qc.cz(1, 2)

	return qc