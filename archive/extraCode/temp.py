import os
import ast
import numpy as np

for filename in os.listdir('IonQAria'):
    with open(f'IonQAria/{filename}') as file:
        data = file.read()

    dict = ast.literal_eval(data)

    max = 0
    for val in dict.keys():
        if int(val) > max:
            max = int(val)
    print(filename, '\t', np.round(np.log2(max + 1))/2)