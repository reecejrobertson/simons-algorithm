import numpy as np
from matplotlib import pyplot as plt

n = 7
N = 2**n
M = 100000
error_probs = [0.0, 0.005, 0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]

vals = [f'{i:0{n}b}' for i in range(N)]
dist = dict.fromkeys(vals, 0.0)
dist['0001000'] = 0.0625
dist['0001011'] = 0.0625
dist['0001100'] = 0.0625
dist['0001111'] = 0.0625
dist['0010000'] = 0.0625
dist['0010011'] = 0.0625
dist['0010100'] = 0.0625
dist['0010111'] = 0.0625
dist['0101000'] = 0.0625
dist['0101011'] = 0.0625
dist['0101100'] = 0.0625
dist['0101111'] = 0.0625
dist['1010000'] = 0.0625
dist['1010011'] = 0.0625
dist['1010100'] = 0.0625
dist['1010111'] = 0.0625

for i, p in enumerate(error_probs):
    new_dist = dict.fromkeys(vals, 0.0)
    draws = np.random.choice(vals, M, p=np.array(list(dist.values())))
    for draw in draws:
        bits = list(draw)
        bits = np.array([int(i) for i in bits])
        perturb = np.random.binomial(1, p, size=n)
        new_bits = (bits + perturb) % 2
        new_draw = ''.join([str(i) for i in new_bits])
        new_dist[str(new_draw)] += 1

    for val in vals:
        new_dist[val] /= M

    plt.figure(figsize=(12,6))
    plt.bar(range(len(new_dist)), list(new_dist.values()), align='center')
    plt.xticks(range(len(new_dist)), list(new_dist.keys()), rotation=45, ha='right', fontsize=4)
    plt.ylabel('Probability', fontsize=16)
    plt.title(f'Simon\'s Algorithm with {p}% Chance of Error', fontsize=20)
    plt.savefig(f'Figures/simons{str(i)}.png', dpi=600)