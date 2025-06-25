import numpy as np
from matplotlib import pyplot as plt

def initialize(n):
    superposition = []
    for i in range(2**n):
        bitstring = []
        for j in range(n):
            if (i % 2 == 1):
                bitstring.append('1')
            else:
                bitstring.append('0')
            i = int(i / 2)
        bitstring.reverse()
        superposition.append(''.join(bitstring))
    return superposition


def selectS(superposition):
    s = np.random.choice(superposition[1:])
    n = len(s)
    sPerp = []
    for x in superposition:
        if sum([(int(x[i]) * int(s[i])) for i in range(n)]) % 2 == 0:
            sPerp.append(x)
    return s, sPerp

def sampleN(sPerp, m):
    n = len(sPerp[0])
    zero = sPerp[0]
    draws = set()
    for i in range(m):
        draw = np.random.choice(sPerp)
        if draw != zero:
            draws.add(draw)
    return draws, len(draws) >= (n - 1)

def sampleUnitlDone(sPerp, shots=1000):
    pass

def sampleNExperiment(a=0, shots=1000):
    for n in range(3, 11):
        m = n + a
        successRate = 0
        for i in range(shots):
            superposition = initialize(n)
            s, sPerp = selectS(superposition)
            draws, success = sampleN(sPerp, n)
            if success:
                successRate += 1
        print(f'{n} qubits, {m} circuit evaluation, {shots} shots, success probability={successRate/shots}')

sampleNExperiment()