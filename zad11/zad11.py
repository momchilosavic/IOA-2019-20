import numpy as np
import math
import matplotlib.pyplot as plt


MMAX = 10
NINT = 3

def dist(A, B):
    sum = 0
    for i in range(len(A)):
        sum += math.pow(A[i]-B[i], 2)
    return math.sqrt(sum)

def opt(x):
    S1 = np.array(x[:3])
    S2 = np.array(x[3:])
    A, B, C, D = np.array([[1, 5, 1], [3, 2,, 0], [5, 6, 1], [6, 3, 3]])
    return dist(A, S1) + dist(B, S1) + dist(S1, S2) + dist(C, S2) + dist(D, S2)


#########################################

def de(fobj, bounds, mut=0.8, crossp=0.9, popsize=50, its=200):
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
        
bnds = [(np.nextafter(0, 1), 10)] * NINT*2
result = list(de(opt, bnds))
print(result[-1])

x,f = zip(*result)
plt.plot(f)

dim = result[-1][0]
S1 = np.zeros((3))
S2 = np.zeros((3))
S1[0] = dim[0]
S1[1] = dim[1]
S1[2] = dim[2]
S2[0] = dim[3]
S2[1] = dim[4]
S2[2] = dim[5]


A, B, C, D = np.array([[1, 5, 1], [2, 3, 0], [5, 6, 1], [6, 3, 3]])

fig = plt.figure(figsize=((8,6)), dpi=80)
ax = fig.add_subplot(111, projection='3d')
ax.scatter(A[0], A[1], A[2])
ax.scatter(B[0], B[1], B[2])
ax.scatter(C[0], C[1], C[2])
ax.scatter(D[0], D[1], D[2])
ax.scatter(S1[0], S1[1], S1[2])
ax.scatter(S2[0], S2[1], S2[2])
plt.plot([A[0], S1[0]], [A[1],S1[1]], [A[2], S1[2]])
plt.plot([B[0], S1[0]], [B[1],S1[1]], [B[2], S1[2]])
plt.plot([S2[0], S1[0]], [S2[1],S1[1]], [S2[2], S1[2]])
plt.plot([C[0], S2[0]], [C[1],S2[1]], [C[2], S2[2]])
plt.plot([D[0], S2[0]], [D[1],S2[1]], [D[2], S2[2]])
#ax.view_init(45, 60)
plt.show()
