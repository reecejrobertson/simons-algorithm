import os
import ast
import numpy as np
from qiskit.result import QuasiDistribution
from matplotlib import pyplot as plt

# TODO: Comments/docstrings.

def plotLine(
        directory, isReversed, isProbabilityFormat,
        shots, lineStyle, label, ticks=False
    ):

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

        resultsDict = None

        if isProbabilityFormat:

            extractedData = ast.literal_eval(data)
            if type(extractedData) == list:
                extractedData = extractedData[0]
            quasiDist = QuasiDistribution(extractedData, shots=shots)
            resultsDict = quasiDist.nearest_probability_distribution()
            resultsDict = resultsDict.binary_probabilities()

            probSum = 0
            for result, prob in resultsDict.items():
                probSum += prob
            assert abs(probSum-1) <= 0.0001, f'Probability incorrect: {probSum}'

        else:
            resultsDict = ast.literal_eval(data)

        errorCount = 0

        for result, frequency in resultsDict.items():
            key = result[numQubits:]
            if isReversed:
                result = result[::-1]
            isOrthogonal = (
                sum([
                    int(key[i]) * int(secretKey[i]) for i in range(numQubits)
                ]) % 2
            ) == 0
            if not isOrthogonal:
                errorCount += frequency

        errorArray[int(numQubits) - 2] += errorCount

    if isProbabilityFormat:
        errorArray /= iterations
    else:
        errorArray /= (shots * iterations)
    errorArray = np.trim_zeros(errorArray)

    qubitCounts = np.arange(4, 2*len(errorArray)+3, 2)

    plt.plot(qubitCounts, errorArray*100, lineStyle, label=label, linewidth=2)
    if ticks:
        plt.xticks(qubitCounts)

def constructPlot(deviceNames, figureName, specialColors=False):

    fig = plt.figure()

    for deviceName in deviceNames:
        directory = 'data/' + deviceName.replace(' ', '')
        isReversed = True if 'IBM' in deviceName else False
        isProbabilityFormat = True if (
            'IBM' in deviceName or 'Aria' in deviceName
        ) and not 'Simulator' in deviceName else False
        shots = 8192 if not 'Forte' in deviceName else 4096
        if specialColors:
            lineStyle = 'ko-' if 'Simulator' not in deviceName else 'rd-'
        else:
            lineStyle = 'o-' if 'Simulator' not in deviceName else 'd-'
        plotLine(
            directory, isReversed, isProbabilityFormat,
            shots, lineStyle, deviceName, True
        )

    plt.xlabel('Number of Qubits')
    plt.ylabel('Percentage of Invalid Outputs')
    plt.legend(loc='best')
    plt.savefig(f'figures/{figureName}', dpi=300)

constructPlot(
    ['IBM Brisbane Simulator', 'IBM Brisbane'], 'IBMBrisbane.png', True
)
constructPlot(['IBM Osaka Simulator', 'IBM Osaka'], 'IBMOsaka.png', True)
constructPlot(['IBM Kyoto Simulator', 'IBM Kyoto'], 'IBMKyoto.png', True)
# constructPlot(
#     ['IBonQ Harmony', 'IBonQ Harmony Simulator'], 'IonQHarmony.png', True
# )
constructPlot(['IonQ Aria Simulator', 'IonQ Aria'], 'IonQAria.png', True)
constructPlot(['IonQ Forte'], 'IonQForte.png', True)
constructPlot(['IBM Brisbane', 'IBM Osaka', 'IBM Kyoto'], 'IBMDevices.png')
constructPlot(
    ['IBM Brisbane Simulator', 'IBM Osaka Simulator', 'IBM Kyoto Simulator'],
    'IBMSimulators.png'
)
constructPlot(['IonQ Aria', 'IonQ Forte'], 'IonQDevices.png')
# constructPlot(['IonQ Harmony', 'IonQ Aria', 'IonQ Forte'], 'IonQDevices.png')
constructPlot(
    ['IonQ Harmony Simulator', 'IonQ Aria Simulator'], 'IonQSimulators.png'
)