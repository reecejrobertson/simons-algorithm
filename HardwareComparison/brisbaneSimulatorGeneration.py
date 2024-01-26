from qiskit import transpile
from qiskit import QuantumCircuit
from qiskit.providers.ibmq import IBMQ
from qiskit_aer.aerprovider import AerSimulator

# Define the needed constants.
N = 8
ITER = 30
SHOTS = 8192

# Load the account with the provided API token.
with open('../IBM_API.txt', 'r') as file:
    token = file.read()
IBMQ.save_account(token=token, overwrite=True)
provider = IBMQ.load_account()

# For each iteration:
for i in range(1, ITER+1):
    print(f'Iteration {i} of {ITER}:')
 
    # Generate a noisy simulator with the latest calibration results.
    backend = provider.get_backend('ibm_brisbane')
    backend = AerSimulator.from_backend(backend)

    # For each problem size:
    for n in range(2, N+1):
        print(f'\t{n} qubits')

        # Create the circuit for this run on Simon's algorithm.
        circuit = QuantumCircuit(2*n)
        for m in range(n):
            circuit.h(m)
        circuit.barrier()
        for m in range(n):
            circuit.cx(m, n+m)
        for m in range(n):
            circuit.cx(0, n+m)
        circuit.barrier()
        for m in range(n):
            circuit.h(m)
        circuit.barrier()
        circuit.measure_all()

        # For each optimization level.
        for level in range(4):

            # Transpile the ideal circuit to an executable circuit.
            transpiled_circuit = transpile(
                circuit, backend, optimization_level=level
            )

            # Run the transpiled circuit using the simulated fake backend.
            job = backend.run(transpiled_circuit, shots=SHOTS)
            result = job.result().get_counts()

            # Save the results to a file.
            with open(
                f'IBMBrisbaneSimulator/n{n}l{level}i{i}.txt', 'w+'
            ) as file:
                file.write(str(result))