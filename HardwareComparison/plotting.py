import os
import ast
import numpy as np
from matplotlib import pyplot as plt

brisbaneDir = 'IBMBrisbane'
brisbaneDir2 = 'IBMBrisbane2'
brisbaneSimDir = 'IBMBrisbaneSimulator'
ariaSimDir = 'IonQAriaSimulator'
harmonySimDir = 'IonQHarmonySimulator'
shots = 8192
brisbaneRepetitions = 10
ionqRepetitions = 30

brisbaneError = np.zeros(11)
brisbaneError2 = np.zeros(11)
brisbaneSimError = np.zeros(11)
ariaSimError = np.zeros(11)
harmonySimError = np.zeros(11)
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

for filename in os.listdir(brisbaneDir2):

    numQubits = int(filename[6:-4])
    secretKey = '1' * numQubits

    file = os.path.join(brisbaneDir2, filename)
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

    brisbaneError2[int(numQubits) - 2] = errorCount/shots

for filename in os.listdir(brisbaneSimDir):

    optimization = int(filename[filename.find('l')+1:filename.find('i')])
    if optimization == 2:
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

        brisbaneSimError[int(numQubits) - 2] += errorCount

brisbaneSimError /= (shots * brisbaneRepetitions)

for filename in os.listdir(ariaSimDir):

    mitigation = int(filename[-7])
    sharpening = int(filename[-5])
    if mitigation == 0 and sharpening == 0:
        numQubits = int(filename[1:filename.find('i')])
        secretKey = '1' * numQubits

        file = os.path.join(ariaSimDir, filename)
        with open(file, 'r') as fin:
            data = fin.read()

        countsDict = ast.literal_eval(data)

        errorCount = 0

        for key, value in countsDict.items():
            actualKey = key[numQubits:]
            isOrthogonal = (sum([int(actualKey[i]) * int(secretKey[i]) for i in range(numQubits)]) % 2) == 0
            if not isOrthogonal:
                errorCount += value

        ariaSimError[int(numQubits) - 2] += errorCount

ariaSimError /= (shots * ionqRepetitions)

for filename in os.listdir(harmonySimDir):

    mitigation = int(filename[-7])
    sharpening = int(filename[-5])
    if mitigation == 0 and sharpening == 0:
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

        harmonySimError[int(numQubits) - 2] += errorCount

harmonySimError /= (shots * ionqRepetitions)

plt.plot(qubitCounts, brisbaneError*100, '.-', label='IBM Brisbane')
plt.plot(qubitCounts[:9], brisbaneError2[:9]*100, '.-', label='IBM Brisbane Repeat')
plt.plot(qubitCounts[:7], brisbaneSimError[:7]*100, '.-', label='IBM Brisbane Simulator')
plt.plot(qubitCounts, ariaSimError*100, '.-', label='IonQ Aria Simulator')
plt.plot(qubitCounts[:4], harmonySimError[:4]*100, '.-', label='IonQ Harmony Simulator')
plt.xticks(qubitCounts)
plt.xlabel('Number of Qubits')
plt.ylabel('Percentage of Invalid Outputs')
plt.legend(loc='best')
plt.savefig('errorComparison.png', dpi=300)