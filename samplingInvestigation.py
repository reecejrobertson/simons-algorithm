import numpy as np
from matplotlib import pyplot as plt

def sample(s, shots=10000):
    print(f'Begin s={s}')
    secretKey = [int(digit) for digit in s]
    n = len(secretKey)
    xVals = np.arange(n-1, n+21)
    xticks = np.arange(n-1, n+21, 2)
    subset = dict()
    successCount = np.zeros_like(xVals)

    for k in range(2**n):
        key = np.zeros(n)
        label = bin(k)[2:][::-1]
        for j in range(len(label)):
            if int(label[j]) == 1:
                key[j] = 1
        isOrthogonal = (
            sum([
                    int(key[i]) * int(secretKey[i]) for i in range(n)
                ]) % 2
            ) == 0
        if isOrthogonal:
            subset[k] = key

    for i, x in enumerate(xVals):
        for shot in range(shots):
            samples = np.random.choice(list(subset.keys()), size=x, replace=True, p=None)
            matrix = np.array([subset[i] for i in samples])
            rank = np.linalg.matrix_rank(matrix)
            if rank >= n-1:
                successCount[i] += 1

    successCount = successCount / shots
        
    fig = plt.figure()
    plt.plot(xVals, successCount)
    plt.xlabel('Number of Samples')
    plt.ylabel('Percentage of Successes')
    plt.xticks(xticks)
    plt.title(f'Sampling with $s={s}$')
    plt.savefig(f'figures/sample{s}.png', dpi=300)
    print(f'Finish s={s}')

sample('11')
sample('111')
sample('1111')
sample('11111')
sample('111111')
sample('1111111')
sample('11111111')
sample('111111111')
sample('1111111111')
sample('11111111111')
sample('111111111111')