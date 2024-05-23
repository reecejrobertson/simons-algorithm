import os
import json
import pandas as pd

def extractData(inputDirectory, outputDirectory):
    for fileName in os.listdir(inputDirectory):
        numQubits = int(fileName[1:fileName.find('i')])
        df = pd.read_csv(inputDirectory + '/' + fileName)
        data = dict()
        usedQubitCount = 2 * numQubits
        if (numQubits) < 5:
            for index, row in df.iterrows():
                result = str(row['Measurement outcome'])
                result = ('0' * (usedQubitCount - len(result))) + result
                count = int(row['Frequency'])
                data[result] = count
        else:
            for index, row in df.iterrows():
                result = int(row['Measurement outcome'], 16)
                result = format(result, f'0>{usedQubitCount}b')
                count = int(row['Frequency'])
                data[result] = count
        with open(outputDirectory + '/' + fileName[:-3] + 'txt', 'w+') as file:
            file.write(json.dumps(data))

# extractData('data/IBMOsakaSimpleCSV', 'data/IBMOsakaSimple')
# extractData('data/IBMOsakaPostUpdateCSV', 'data/IBMOsakaPostUpdate')