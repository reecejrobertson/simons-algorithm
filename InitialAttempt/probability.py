import numpy as np

def p(n, k):
    return 1. - 1./(2.**(n-k))

def q(n, k):
    return 1./(2.**(n-k))

def prob(n, k):
    base = np.prod([p(n, i) for i in range(k)])
    possibilites = generatePossibilities(n - k, k + 1)
    ans = 0
    for poss in possibilites:
        ans += base * np.prod([q(n, k) for k in poss])
    return ans

def generatePossibilities(n, upper):
    curr = [0] * n
    possibilites = [curr.copy()]
    while True:
        curr = increment(curr, upper)
        possibilites.append(curr.copy())
        if curr == [upper] * n:
            break
    return possibilites

def increment(curr, upper):
    n = len(curr)
    i = n - 1
    curr[i] += 1
    while curr[i] > upper:
        curr[i-1] += 1
        i -= 1
    for j in range(i + 1, n):
        curr[j] = curr[i]
    return curr

print(prob(13, 10))