import time
import warnings
from qiskit import transpile
from qiskit import QuantumCircuit
from qiskit_ionq import IonQProvider, ErrorMitigation
from qiskit.providers.jobstatus import JobStatus

# Suppress warnings (error mitigation on simulator produces user warning).
warnings.filterwarnings("ignore")

# Define the needed constants.
N = 2
ITER = 1
SHOTS = 8192

# Load the account with the provided API token.
with open('../../APIs/IonQ_Paid_API.txt', 'r') as file:
    token = file.read()
provider = IonQProvider(token)

# Get the IonQ Aria1 noisy backend.
backend = provider.get_backend('ionq_qpu.harmony')

with open('../extraData/harmonyIds.txt') as file:
    jobIds = file.readlines()

for id in jobIds:
    job = backend.retrieve_job(id.strip())
    print(job.result().get_counts())
