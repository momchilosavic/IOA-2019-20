import numpy as np
import math
import time


##### PARAMS ##################################################################

Zp = complex(100, -100)
C0 = 299792458
N = 3
Z0 = 50

P_MAX = -20

F_MIN = 800*1000000
F_MAX = 1200*1000000
F_STEP = 1*1000000

L_MIN = 30/1000
L_MAX = 110/1000

ZC_MIN = 20
ZC_MAX = 120

###############################################################################

Zc = np.random.random(N) * (ZC_MAX - ZC_MIN) + ZC_MIN
l = np.random.random(N) * (L_MAX - L_MIN) + L_MIN
f = np.arange(F_MIN, F_MAX + F_STEP, F_STEP)

###############################################################################

###############################################################################

##### FUNCTIONS ###############################################################

def Beta(f):
    return 2*math.pi*f/C0

def Zout(Zin, Zc, l, f):
    return Zc * (Zin + complex(0, Zc*math.tan(Beta(f) * l))) / (Zc + Zin * complex(0, math.tan(Beta(f) * l)))

def pDb(Z):
    return 20*math.log10(abs((Z - Z0)/(Z + Z0)))

def fun(f, Zc, l):
    Zin = Zp
    for k in range(N):
        Zin = Zout(Zin, Zc[k], l[k], f)
    return Zin

    
def opt(vars):
    sum = 0;
    Zc, l = vars[:N], vars[N:]
    for i in range(len(f)):
        fff = pDb(fun(f[i], Zc, l))
        if(fff <= P_MAX):
            #print(fff)
            sum-=1
    return sum


#########################################

def de(fobj, bounds, mut=0.8, crossp=0.9, popsize=50, its=100):
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
            idxs = [idx for idx in range(popsize) if idx != j]                  # selekcija
            a, b, c = pop[np.random.choice(idxs, 3, replace = False)]
            mutant = np.clip(a + mut * (b - c), 0, 1)                           # ukrstanje 
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
            #print(fitness[best_idx])
        yield best, fitness[best_idx]
        
bnds = [(ZC_MIN, ZC_MAX)] * N
bnds += [(L_MIN, L_MAX)] * N
start_time = time.time()
result = list(de(opt, bnds))
elapsed_time = time.time() - start_time
print('Elapsed time: ', elapsed_time)
print(result[-1])
