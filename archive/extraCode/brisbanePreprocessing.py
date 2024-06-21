import os
import ast
import numpy as np
from matplotlib import pyplot as plt

brisbaneDir = 'IBMBrisbane'
brisbaneSimDir = 'IBMBrisbaneSimulator'
shots = 8192
repetitions = 10

brisbaneError = np.zeros(11)
brisbaneSimError0 = np.zeros(11)
brisbaneSimError1 = np.zeros(11)
brisbaneSimError2 = np.zeros(11)
brisbaneSimError3 = np.zeros(11)
qubitCounts = np.arange(4, 25, 2)

for filename in os.listdir(brisbaneDir):

    numQubits = int(filename[6:-4])
    secretKey = '1' * numQubits

    file = os.path.join(brisbaneDir, filename)
    with open(file, 'r') as fin:
        data = fin.read()

    data = data.replace('\n', '').replace('\t', '')[1:-1]
    dataDict = ast.literal_eval(data)

    for key in dataDict:
        assert len(key) == 2*numQubits
        break

    probDict = dict()
    probSum = 0

    for key, value in dataDict.items():
        if value < 0:
            probDict[key] = 0
        else:
            probDict[key] = value
            probSum += value

    countsDict = dict()
    countsSum = 0

    for key, value in probDict.items():
        count = round((value / probSum) * shots)
        countsDict[key] = count
        countsSum += count

    errorCount = 0

    for key, value in countsDict.items():
        actualKey = key[::-1][:numQubits]
        isOrthogonal = (sum([int(actualKey[i]) * int(secretKey[i]) for i in range(numQubits)]) % 2) == 0
        if not isOrthogonal:
            errorCount += value

    brisbaneError[int(numQubits) - 2] = errorCount/shots

for filename in os.listdir(brisbaneSimDir):

    optimization = int(filename[filename.find('l')+1:filename.find('i')])
    numQubits = int(filename[1:filename.find('l')])
    secretKey = '1' * numQubits

    file = os.path.join(brisbaneSimDir, filename)
    with open(file, 'r') as fin:
        data = fin.read()

    countsDict = ast.literal_eval(data)

    errorCount = 0

    for key, value in countsDict.items():
        actualKey = key[::-1][:numQubits]
        isOrthogonal = (sum([int(actualKey[i]) * int(secretKey[i]) for i in range(numQubits)]) % 2) == 0
        if not isOrthogonal:
            errorCount += value

    if optimization == 0:
        brisbaneSimError0[int(numQubits) - 2] += errorCount
    if optimization == 1:
        brisbaneSimError1[int(numQubits) - 2] += errorCount
    if optimization == 2:
        brisbaneSimError2[int(numQubits) - 2] += errorCount
    if optimization == 3:
        brisbaneSimError3[int(numQubits) - 2] += errorCount

brisbaneSimError0 /= (shots * repetitions)
brisbaneSimError1 /= (shots * repetitions)
brisbaneSimError2 /= (shots * repetitions)
brisbaneSimError3 /= (shots * repetitions)

plt.plot(qubitCounts, brisbaneError*100, '.-', label='Brisbane True Data')
plt.plot(qubitCounts[:7], brisbaneSimError0[:7]*100, '.-', label='Brisbane Simulator Optimization 0')
plt.plot(qubitCounts[:7], brisbaneSimError1[:7]*100, '.-', label='Brisbane Simulator Optimization 1')
plt.plot(qubitCounts[:7], brisbaneSimError2[:7]*100, '.-', label='Brisbane Simulator Optimization 2')
plt.plot(qubitCounts[:7], brisbaneSimError3[:7]*100, '.-', label='Brisbane Simulator Optimization 3')
plt.xticks(qubitCounts)
plt.xlabel('Number of Qubits')
plt.ylabel('Percentage of Invalid Outputs')
plt.legend(loc='best')
plt.title('Simon\'s Algorithm IBM Error Rate Comparison (8192 shots)')
plt.savefig('brisbaneError.png', dpi=300)