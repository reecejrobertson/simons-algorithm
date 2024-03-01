import os
import ast
import numpy as np
from matplotlib import pyplot as plt

brisbaneDir = 'IBMBrisbane'
brisbaneSimDir = 'IBMBrisbaneSimulator'
ariaSimDir = 'IonQAriaSimulator'
harmonySimDir = 'IonQHarmonySimulator'
shots = 8192
brisbaneReps = 3
brisbaneRepetitions = 10
ionqRepetitions = 30

brisbaneError = np.zeros(11)
brisbaneSimError = np.zeros(11)
ariaSimError = np.zeros(11)
harmonySimError = np.zeros(11)
qubitCounts = np.arange(4, 25, 2)

def plotLine(directory, isReversed, isProbabilityFormat, shots, lineStyle, label):

    errorArray = np.zeros(100)
    iterations = 0
    for filename in os.listdir(directory):
        
        numQubits = int(filename[1:filename.find('i')])
        secretKey = '1' * numQubits

        iteration = int(filename[filename.find('i')+1:-4])
        if iteration > iterations:
            iterations = iteration

        file = os.path.join(directory, filename)
        with open(file, 'r') as fin:
            data = fin.read()

        countsDict = None

        if isProbabilityFormat:
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

        else:
            countsDict = ast.literal_eval(data)

        errorCount = 0

        for key, value in countsDict.items():
            if isReversed:
                key = key[::-1]
            key = key[:numQubits]
            isOrthogonal = (sum([int(key[i]) * int(secretKey[i]) for i in range(numQubits)]) % 2) == 0
            if not isOrthogonal:
                errorCount += value

        errorArray[int(numQubits) - 2] += errorCount

    errorArray /= shots * iterations
    errorArray = np.trim_zeros(errorArray)

    qubitCounts = np.arange(4, 2*len(errorArray), 2)

    plt.plot(qubitCounts, errorArray*100, lineStyle, label=label)


plt.xticks(qubitCounts)
plt.xlabel('Number of Qubits')
plt.ylabel('Percentage of Invalid Outputs')
plt.legend(loc='best')
plt.savefig('IBMError.png', dpi=300)