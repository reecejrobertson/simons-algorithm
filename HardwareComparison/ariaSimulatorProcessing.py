import os
import ast
import numpy as np
from matplotlib import pyplot as plt

dir = 'IonQAriaSimulator'
shots = 8192
repetitions = 30

mitigation0sharpening0 = np.zeros(11)
mitigation0sharpening1 = np.zeros(11)
mitigation1sharpening0 = np.zeros(11)
mitigation1sharpening1 = np.zeros(11)
qubitCounts = np.arange(4, 25, 2)

for filename in os.listdir(dir):

    mitigation = int(filename[-7])
    sharpening = int(filename[-5])
    numQubits = int(filename[1:filename.find('i')])
    secretKey = '1' * numQubits

    file = os.path.join(dir, filename)
    with open(file, 'r') as fin:
        data = fin.read()

    countsDict = ast.literal_eval(data)

    errorCount = 0

    for key, value in countsDict.items():
        actualKey = key[numQubits:]
        isOrthogonal = (sum([int(actualKey[i]) * int(secretKey[i]) for i in range(numQubits)]) % 2) == 0
        if not isOrthogonal:
            errorCount += value

    if mitigation == 0 and sharpening == 0:
        mitigation0sharpening0[int(numQubits) - 2] += errorCount
    elif mitigation == 0 and sharpening == 1:
        mitigation0sharpening1[int(numQubits) - 2] += errorCount
    elif mitigation == 1 and sharpening == 0:
        mitigation1sharpening0[int(numQubits) - 2] += errorCount
    elif mitigation == 1 and sharpening == 1:
        mitigation1sharpening1[int(numQubits) - 2] += errorCount
    else:
        print('Mitigation and/or sharpening value read incorrectly.')
        exit(1)

mitigation0sharpening0 /= (shots * repetitions)
mitigation0sharpening1 /= (shots * repetitions)
mitigation1sharpening0 /= (shots * repetitions)
mitigation1sharpening1 /= (shots * repetitions)

plt.plot(qubitCounts, mitigation0sharpening0*100, '.-', label='Not Mitigated and Not Sharpened')
plt.plot(qubitCounts, mitigation0sharpening1*100, '.-', label='Not Mitigated and Sharpened')
plt.plot(qubitCounts, mitigation1sharpening0*100, '.-', label='Mitigated and Not Sharpened')
plt.plot(qubitCounts, mitigation1sharpening1*100, '.-', label='Mitigated and Sharpened')
plt.xticks(qubitCounts)
plt.xlabel('Number of Qubits')
plt.ylabel('Percentage of Invalid Outputs')
plt.legend(loc='best')
plt.title(f'Simon\'s Algorithm Error Rate on IonQ Aria Simulator ({shots} shots, {repetitions} repetitions)')
plt.savefig('IonQAriaSimulatorError.png', dpi=300)