import os
import ast
import numpy as np
from qiskit.result import QuasiDistribution
from matplotlib import pyplot as plt

def plotLine(
        directory, isReversed, isProbFormat,
        shots, lineStyle, label, ticks=False
    ):
    '''
    A function to evaluate and plot an error line for a device.
    Parameters:
        directory (string)      : The name of the directory to extract and plot.
        isReversed (Boolean)    : Indicates if the result strings are inverted.
        isProbFormat (Boolean)  : Indicates if frequencies are probabilities.
        shots (int)             : The number of times each job was repeated.
        lineStyle (string)      : The style of the line to plot.
        label (string)          : The label of the line to plot.
        ticks (Boolean)         : Indicates if x-ticks should be plotted.
    '''

    # Initialize empty needed variables.
    errorArray = np.zeros(100)
    iterations = 0

    # For each file in the directory:
    for filename in os.listdir(directory):

        # Initialize empty needed variables.
        resultsDict = None
        errorCount = 0

        # Extract the number of qubits and iteration number from the filename.
        numQubits = int(filename[1:filename.find('i')])
        iteration = int(filename[filename.find('i')+1:-4])

        # Update the maximum iteration if needed.
        if iteration > iterations:
            iterations = iteration
            
        # Compose the secret key from the number of qubits.
        secretKey = '1' * numQubits

        # Read the data from the working file.
        file = os.path.join(directory, filename)
        with open(file, 'r') as fin:
            data = fin.read()

        # If this file is in probability format:
        if isProbFormat:

            # Extract the data and obtain the nearest probability distribution.
            extractedData = ast.literal_eval(data)
            if type(extractedData) == list:
                extractedData = extractedData[0]
            quasiDist = QuasiDistribution(extractedData, shots=shots)
            resultsDict = quasiDist.nearest_probability_distribution()
            resultsDict = resultsDict.binary_probabilities()

            # Assert that the probabilities sum to unity (approximately).
            probSum = 0
            for result, prob in resultsDict.items():
                probSum += prob
            assert abs(probSum-1) <= 0.0001, f'Probability incorrect: {probSum}'

        # Otherwise if this file is not in probability format:
        else:
            
            # Extract the data as is.
            resultsDict = ast.literal_eval(data)

        # For each key-value pair in the data:
        for result, frequency in resultsDict.items():

            # Extract the secret key (reversing if necessary).
            # Note that because our secret key is always symmetric (it is the
            # string of all 1's), we do not need to reverse the key here.
            # However, reversing is required in general when needed.
            key = result[numQubits:]
            if isReversed:
                result = result[::-1]

            # Identify if the extracted key is orthogonal to the secret key.
            isOrthogonal = (
                sum([
                    int(key[i]) * int(secretKey[i]) for i in range(numQubits)
                ]) % 2
            ) == 0

            # Increment the error count for strings that are not orthogonal.
            if not isOrthogonal:
                errorCount += frequency

        # Finally, update the error count with the data from the file.
        errorArray[int(numQubits) - 2] += errorCount

    # Normalize the error counts by dividing by the number of iterations.
    if isProbFormat:
        errorArray /= iterations
    else:
        errorArray /= (shots * iterations)

    # Trim the error array and create a qubit count array of the proper size.
    errorArray = np.trim_zeros(errorArray)
    qubitCounts = np.arange(2, len(errorArray)+2, 1)

    # Plot the error array against the qubit count array.
    plt.plot(qubitCounts, errorArray*100, lineStyle, label=label, linewidth=2)

    # Plot x-ticks if requested.
    if ticks:
        plt.xticks(qubitCounts)

def constructPlot(deviceNames, figureName, specialColors=False):
    '''
    A function to create a plot featuring listed devices.
    Parameters:
        deviceNames (array)     : A list of the device names to include.
        figureName (array)      : The name under which to save the figure.
        specialColors (Boolean) : Indicates if colors should be used to
                                  differentiate between devices and simulators.
    '''

    # Define a new figure on which to plot.
    fig = plt.figure()

    # For each provided device:
    for deviceName in deviceNames:

        # Define the inputs for the plotLine function.
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

        # Plot the error count line using the plotLine function.
        plotLine(
            directory, isReversed, isProbabilityFormat,
            shots, lineStyle, deviceName, True
        )

    # Label and save the plot.
    plt.xlabel('Problem Size ($n$)')
    plt.ylabel('Algorithmic Error')
    plt.legend(loc='best')
    plt.savefig(f'figures/{figureName}', dpi=300)

# Calls to plot the lines from the collected data.
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
