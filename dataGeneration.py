import time
import warnings
from qiskit import transpile
from qiskit import QuantumCircuit
from qiskit_ionq import IonQProvider
from qiskit.providers.jobstatus import JobStatus
from qiskit.providers.ibmq import IBMQ
from qiskit_aer.aerprovider import AerSimulator

# Suppress warnings (error mitigation on IonQ simulator produces user warning).
warnings.filterwarnings("ignore")

def executeSimons(
        apiToken, device, directory,
        N=12, iterations=30, shots=8192, sleepTime=5
    ):
    '''
    A function to run Simon's algorithm on various hardware platforms.
    Parameters:
        apiToken (string)   : The API token used for access.
        device (string)     : The name of the device on which to run.
        directory (string)  : The name of the directory in which to save data.
        N (int)             : Defines the size of the largest job (2*N).
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
    if 'IonQ' in apiToken:
        provider = IonQProvider(token)
    elif 'IBM' in apiToken:
        IBMQ.save_account(token=token, overwrite=True)
        provider = IBMQ.load_account()
    else:
        raise ValueError('Invalid API token provided.')

    # For each iteration:
    for i in range(1, iterations+1):
        print(f'Iteration {i} of {iterations}:')

        # Get a backend. Can be IBM simulators and IonQ devices and simulators.
        backend = None
        match device.lower():
            case 'harmony':
                backend = provider.get_backend('ionq_qpu')
            case 'aria':
                backend = provider.get_backend('ionq_qpu')
            case 'harmonysimulator':
                backend = provider.get_backend('ionq_simulator')
                backend.set_options(noise_model='harmony')
            case 'ariasimulator':
                backend = provider.get_backend('ionq_simulator')
                backend.set_options(noise_model='aria-1')
            case 'brisbane':
                backend = provider.get_backend('ibm_brisbane')
            case 'brisbanesimulator':
                backend = provider.get_backend('ibm_brisbane')
                backend = AerSimulator.from_backend(backend)
            case 'osaka':
                backend = provider.get_backend('ibm_osaka')
            case 'osakasimulator':
                backend = provider.get_backend('ibm_osaka')
                backend = AerSimulator.from_backend(backend)
            case 'kyoto':
                backend = provider.get_backend('ibm_kyoto')
            case 'kyotosimulator':
                backend = provider.get_backend('ibm_kyoto')
                backend = AerSimulator.from_backend(backend)
            case _:
                raise ValueError('Requested device is not supported.')

        # For each problem size:
        for n in range(2, N+1):
            print(f'\t{n} qubits')

            # Create the circuit for this run on Simon's algorithm.
            circuit = QuantumCircuit(2*n)
            for m in range(n):
                circuit.h(m)
            for m in range(n):
                circuit.cx(m, n+m)
            for m in range(n):
                circuit.cx(0, n+m)
                # break   # Uncomment for "simple" oracle.
            for m in range(n):
                circuit.h(m)
            circuit.measure_all()

            # Transpile the ideal circuit to an executable circuit and run it.
            transpiled_circuit = transpile(circuit, backend)
            job = backend.run(transpiled_circuit, shots=shots)

            # # Check if job is done.
            # while job.status() is not JobStatus.DONE:
            #     print('\t\tJob status is', job.status() )
            #     time.sleep(sleepTime)

            # # When it is done, save the results to a file.
            # print('\t\tJob status is', job.status())
            # result = job.result().get_counts()
            # with open(
            #     f'data/{directory}/n{n}i{i}.txt', 'w+'
            # ) as file:
            #     file.write(str(result))

# # Calls to run Simon's algorithm on the various supported backends.
# executeSimons('APIs/IonQ_Paid_API.txt', 'harmony', 'IonQHarmony',
#               N=5, iterations=2, shots=8192, sleepTime=1800)
# executeSimons('APIs/IonQ_Paid_API.txt', 'aria', 'IonQAria',
#               N=12, iterations=1, shots=4096, sleepTime=1800)
# executeSimons('APIs/IonQ_API.txt', 'ariaSimulator', 'IonQAriaSimulator')
# executeSimons('APIs/IonQ_API.txt', 'harmonySimulator', 'IonQHarmonySimulator')
# executeSimons('APIs/IBM_API.txt', 'kyotoSimulator', 'IBMKyotoSimulator',
#               N=7, sleepTime=0.5)
# executeSimons('APIs/IBM_API.txt', 'osakaSimulator', 'IBMOsakaSimulator',
#               N=7, sleepTime=0.5)
# executeSimons('APIs/IBM_API.txt', 'brisbaneSimulator', 'IBMBrisbaneSimulator',
#               N=7, sleepTime=0.5)
# executeSimons('APIs/IBM_API.txt', 'kyotoSimulator', 'IBMKyotoSimulatorSimple',
#               N=7, sleepTime=0.5)
# executeSimons('APIs/IBM_API.txt', 'brisbaneSimulator', 'IBMBrisbaneSimulatorSimple',
#               N=7, sleepTime=0.5)
# executeSimons('APIs/IBM_API.txt', 'kyoto', 'IBMKyotoSimple',
#               iterations=3, sleepTime=30)
# executeSimons('APIs/IBM_API.txt', 'brisbane', 'IBMBrisbaneSimple',
#               iterations=3, sleepTime=30)