import time
from qiskit import transpile
from qiskit import QuantumCircuit
from qiskit.providers.jobstatus import JobStatus
from qiskit.providers.ibmq import IBMQ
from qiskit_aer.aerprovider import AerSimulator

def cnotTest(
        apiToken, device, directory,
        iterations=30, shots=8192, sleepTime=5
    ):
    '''
    Perform a CNOT between qubits of variable distance on IBM devices.
    Parameters:
        apiToken (string)   : The API token used for access.
        device (string)     : The name of the device on which to run.
        directory (string)  : The name of the directory in which to save data.
        iterations (int)    : The number of times to repeat the experiment.
        shots (int)         : The number of iterations for each job.
        sleepTime (int)     : The time to pause while querying job status.
    '''

    # Load the account with the provided API token.
    provider = None
    try:
        with open(apiToken, 'r') as file:
            token = file.read()
    except:
        raise ValueError('Invalid API token provided.')
    if 'IBM' in apiToken:
        IBMQ.save_account(token=token, overwrite=True)
        provider = IBMQ.load_account()
    else:
        raise ValueError('Invalid API token provided.')

    # For each iteration:
    for i in range(1, iterations+1):
        print(f'{device} Iteration {i} of {iterations}:')

        # Get a backend. Can be IBM simulators and IonQ devices and simulators.
        # Note that IBM devices were accessed using the 'Composer' interface.
        backend = None
        match device.lower():
            case 'brisbane':
                backend = provider.get_backend('ibm_brisbane')
            case 'osaka':
                backend = provider.get_backend('ibm_osaka')
            case 'kyoto':
                backend = provider.get_backend('ibm_kyoto')
            case 'brisbanesimulator':
                backend = provider.get_backend('ibm_brisbane')
                backend = AerSimulator.from_backend(backend)
            case 'osakasimulator':
                backend = provider.get_backend('ibm_osaka')
                backend = AerSimulator.from_backend(backend)
            case 'kyotosimulator':
                backend = provider.get_backend('ibm_kyoto')
                backend = AerSimulator.from_backend(backend)
            case _:
                raise ValueError('Requested device is not supported.')

        # For each problem size:
        for n in range(40, 50):
            print(f'\tCX(39,{n})')

            # Create the circuit for this run on Simon's algorithm.
            circuit = QuantumCircuit(127)
            circuit.x(39)
            circuit.cx(39,n)
            circuit.measure_active()

            # Transpile the ideal circuit to an executable circuit and run it.
            transpiled_circuit = transpile(circuit, backend, optimization_level=0)
            job = backend.run(transpiled_circuit, shots=shots)

            # Check if job is done.
            while job.status() is not JobStatus.DONE:
                print('\t\tJob status is', job.status() )
                time.sleep(sleepTime)

            # When it is done, save the results to a file.
            print('\t\tJob status is', job.status())
            result = job.result().get_counts()
            with open(
                f'cnotData/{directory}/n{n}i{i}.txt', 'w+'
            ) as file:
                file.write(str(result))

# Calls to run Simon's algorithm on the various supported backends.
# cnotTest('APIs/IBM_Work_API.txt', 'kyotoSimulator', 'IBMKyotoSimulator',
#               sleepTime=0.5)
# cnotTest('APIs/IBM_Work_API.txt', 'osakaSimulator', 'IBMOsakaSimulator',
#               sleepTime=0.5)
# cnotTest('APIs/IBM_Work_API.txt', 'brisbaneSimulator', 'IBMBrisbaneSimulator',
#               sleepTime=0.5)
# cnotTest('APIs/IBM_Work_API.txt', 'kyoto', 'IBMKyoto',
#               iterations=3)
# cnotTest('APIs/IBM_Work_API.txt', 'osaka', 'IBMOsaka',
#               iterations=3)
# cnotTest('APIs/IBM_Work_API.txt', 'brisbane', 'IBMBrisbane',
#               iterations=3)