import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML


MMAX = 10
NINT = 5

def func(x, m):
    return math.pow(x, m) * math.log(x)
    
def opt(X):
    NINT = int(len(X)/2)
    x = X[:NINT]
    w = X[NINT:]
    sum = 0
    for m in range(1, MMAX+1):
        inner_sum = 0
        for k in range(NINT):
            inner_sum += w[k] * func(x[k], m)
        sum += abs((1/math.pow(m+1, 2) + inner_sum)) / (1/math.pow(m+1, 2))
    return sum/MMAX

def de(fobj, bounds, mut=0.8, crossp=0.9, popsize=50, its=1000):
    dimensions = len(bounds)                    # broj dimenzija
    pop = np.random.rand(popsize, dimensions)   # populacija (0 - 1)
    min_b, max_b = np.asarray(bounds).T         # granice
    diff = np.fabs(min_b - max_b)               # razlika granica
    pop_denorm = min_b + pop * diff             # populacija (min - max)
    
    fitness = np.asarray([fobj(ind) for ind in pop_denorm]) # vrednost funckije
    best_idx = np.argmin(fitness)               # indeks minimalne vrednosti funkcije
    best = pop_denorm[best_idx]                 # minimalna vrednost funkcije
    for i in range(its):
        for j in range(popsize):
            idxs = [idx for idx in range(popsize) if idx != j]
            a, b, c = pop[np.random.choice(idxs, 3, replace = False)]
            mutant = np.clip(a + mut * (b - c), 0, 1)
            cross_points = np.random.rand(dimensions) < crossp
            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True
            trial = np.where(cross_points, mutant, pop[j])
            trial_denorm = min_b + trial * diff
            f = fobj(trial_denorm)
            if f < fitness[j]:
                fitness[j] = f
                pop[j] = trial
                if f < fitness[best_idx]:
                    best_idx = j
                    best = trial_denorm
        yield best, fitness[best_idx]
        
bnds = [(np.nextafter(0, 1), 1)] * NINT
bnds +=[(0,1)] * NINT
result = list(de(opt, bnds))
print(result[-1])

x,f = zip(*result)
plt.plot(f)