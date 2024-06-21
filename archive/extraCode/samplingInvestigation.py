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

def sample2(s, p, shots=10000):
    print(f'Begin s={s} p={p} shots={shots}')
    secretKey = [int(digit) for digit in s]
    n = len(secretKey)
    xVals = np.arange(n-1, n+21)
    xticks = np.arange(-1, 21, 2)
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
            probArray = np.random.uniform(size=x)
            valid = np.sum([probArray > p])
            samples = np.random.choice(list(subset.keys()), size=valid, replace=True, p=None)
            matrix = np.array([subset[i] for i in samples])
            rank = np.linalg.matrix_rank(matrix)
            if rank >= n-1:
                successCount[i] += 1

    successCount = successCount / shots
        
    fig = plt.figure()
    plt.plot(xVals - n, successCount)
    plt.xlabel('$x$')
    plt.ylabel('Percentage of Successes')
    plt.xticks(xticks)
    plt.title(f'Sampling with $s={s}$ & $p={p}$')
    plt.savefig(f'figures2/sampleS{s}P{str(p)[2:]}.png', dpi=300)
    print(f'Finish s={s} p={p}')

pArray = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
for p in pArray:
    sample2('11', p)
    sample2('111', p)
    sample2('1111', p)
    sample2('11111', p)
    sample2('111111', p)
    sample2('1111111', p)
    sample2('11111111', p)
    sample2('111111111', p)
    sample2('1111111111', p)
    sample2('11111111111', p)
    sample2('111111111111', p)


# sample('11')
# sample('111')
# sample('1111')
# sample('11111')
# sample('111111')
# sample('1111111')
# sample('11111111')
# sample('111111111')
# sample('1111111111')
# sample('11111111111')
# sample('111111111111')