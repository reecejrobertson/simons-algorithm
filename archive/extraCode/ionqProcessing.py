import os
import ast
import numpy as np
from matplotlib import pyplot as plt

simDir = 'data/IonQAriaSimulator'
dir = 'data/IonQForte'
harmonySimDir = 'data/IonQHarmonySimulator'
shots = 4096
simShots = 8192
repetitions = 30

array = np.zeros(16)
simArray = np.zeros(11)
harmonySimArray = np.zeros(4)
qubitCounts = np.arange(4, 35, 2)

for filename in os.listdir(dir):

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

    array[int(numQubits) - 2] += errorCount

for filename in os.listdir(simDir):

    # mitigation = int(filename[-7])
    # sharpening = int(filename[-5])
    numQubits = int(filename[1:filename.find('i')])
    secretKey = '1' * numQubits

    file = os.path.join(simDir, filename)
    with open(file, 'r') as fin:
        data = fin.read()

    countsDict = ast.literal_eval(data)

    errorCount = 0

    for key, value in countsDict.items():
        actualKey = key[numQubits:]
        isOrthogonal = (sum([int(actualKey[i]) * int(secretKey[i]) for i in range(numQubits)]) % 2) == 0
        if not isOrthogonal:
            errorCount += value

    # if mitigation == 0 and sharpening == 0:
    simArray[int(numQubits) - 2] += errorCount

for filename in os.listdir(harmonySimDir):

    # mitigation = int(filename[-7])
    # sharpening = int(filename[-5])
    # if mitigation == 0 and sharpening == 0:
    numQubits = int(filename[1:filename.find('i')])
    secretKey = '1' * numQubits

    file = os.path.join(harmonySimDir, filename)
    with open(file, 'r') as fin:
        data = fin.read()

    countsDict = ast.literal_eval(data)

    errorCount = 0

    for key, value in countsDict.items():
        actualKey = key[numQubits:]
        isOrthogonal = (sum([int(actualKey[i]) * int(secretKey[i]) for i in range(numQubits)]) % 2) == 0
        if not isOrthogonal:
            errorCount += value

    harmonySimArray[int(numQubits) - 2] += errorCount

array /= shots
simArray /= (simShots * repetitions)
harmonySimArray /= (simShots * repetitions)

plt.plot(qubitCounts, array*100, '.-', label='Forte')
plt.plot(qubitCounts[:11], simArray*100, '.-', label='Aria Simulator')
plt.plot(qubitCounts[:4], harmonySimArray*100, '.-', label='Harmony Simulator')
plt.xticks(qubitCounts)
plt.xlabel('Number of Qubits')
plt.ylabel('Percentage of Invalid Outputs')
plt.legend(loc='best')
# plt.title(f'Simon\'s Algorithm Error Rate on IonQ')
plt.savefig('IonQError.png', dpi=300)