import os
import ast
import numpy as np
from matplotlib import pyplot as plt

brisbaneDir = 'IBMBrisbane'
washingtonDir = 'IBMWashingtonNoisySimulator'
sherbrookeDir = 'IBMSherbrookeNoisySimulator'
shots = 8192

brisbaneError = np.zeros(11)
sherbrookeError = np.zeros(11)
washingtonError = np.zeros(11)
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

for filename in os.listdir(washingtonDir):

    numQubits = int(filename[6:-4])
    secretKey = '1' * numQubits

    file = os.path.join(washingtonDir, filename)
    with open(file, 'r') as fin:
        data = fin.read()

    countsDict = ast.literal_eval(data)

    errorCount = 0

    for key, value in countsDict.items():
        actualKey = key[::-1][:numQubits]
        isOrthogonal = (sum([int(actualKey[i]) * int(secretKey[i]) for i in range(numQubits)]) % 2) == 0
        if not isOrthogonal:
            errorCount += value

    washingtonError[int(numQubits) - 2] = errorCount/shots

for filename in os.listdir(sherbrookeDir):

    numQubits = int(filename[6:-4])
    secretKey = '1' * numQubits

    file = os.path.join(sherbrookeDir, filename)
    with open(file, 'r') as fin:
        data = fin.read()

    countsDict = ast.literal_eval(data)

    errorCount = 0

    for key, value in countsDict.items():
        actualKey = key[::-1][:numQubits]
        isOrthogonal = (sum([int(actualKey[i]) * int(secretKey[i]) for i in range(numQubits)]) % 2) == 0
        if not isOrthogonal:
            errorCount += value

    sherbrookeError[int(numQubits) - 2] = errorCount/shots

plt.plot(qubitCounts, brisbaneError*100, '.-', label='IBM Brisbane')
plt.plot(qubitCounts[:8], sherbrookeError[:8]*100, '.-', label='IBM Sherbrooke Noisy Simulator')
plt.plot(qubitCounts[:8], washingtonError[:8]*100, '.-', label='IBM WashingtonV2 Noisy Simulator')
plt.xticks(qubitCounts)
plt.xlabel('Number of Qubits')
plt.ylabel('Percentage of Invalid Outputs')
plt.legend(loc='best')
plt.title('Simon\'s Algorithm Hardware Error Rate Comparison (8192 shots)')
plt.savefig('errorComparison.png', dpi=300)