import random
import numpy as np
import matplotlib.pyplot as plt

MIN_GEN = 30
MAX_GEN = 100
MAX_POP = 200000

CROSSING_PROB = 0.8
MUTATION_PROB = 0.1
#CROSSING_COUNT = Npop/5


Npop = 150
Ngen = 50

Nite = Npop * Ngen



def starting_generation(Npop):
    x = np.zeros((Npop, 100))
    for i in range(Npop):
        x[i] = np.random.choice([0,1], 100, p=[0.2, 0.8])
        #x[i] = np.random.randint(2, size=100)
    return x

def function(x):
    sums = np.zeros((len(x)))
    for i in range(len(x)):
        sum = 0
        for j in range (len(x[0])):
            sum += x[i][j]
        sums[i] = sum
    return sums

def selection(x, f, count):
    parents = np.zeros((count, 100))
    indices = np.argpartition(f, count)
    for i in range(count):
        parents[i] = x[indices[i]]
    return parents

def cross(parent1, parent2):
    point = int(random.random() * 100)
    x1 = np.zeros((100))
    x2 = np.zeros((100))
    for i in range(point):
        x1[i] = parent1[i]
        x2[i] = parent2[i]
    for i in range(100-point):
        x1[i] = parent2[point + i]
        x2[i] = parent1[point + i]
    return x1, x2
        

def crossing(parents, prob, Npop):
    cross_number = Npop - len(parents)
    crossover = np.zeros((cross_number, 100))
        
    cross_cnt = 0
    parents_temp = np.zeros((2, 100))
    ind = 0
    while(cross_cnt < cross_number):
        for i in range(len(parents)):
            if(random.random() < prob):
                parents_temp[ind] = parents[i]
                ind = 1 - ind
                if ind == 0:
                    crossover[cross_cnt], \
                    crossover[cross_cnt+1] =\
                    cross(parents_temp[0], parents_temp[1])
                    cross_cnt += 2
                    if(cross_cnt == cross_number):
                        break
    return crossover
                
    
    
    
def mutation(x, prob):
    for i in range(len(x)):
        if(random.random() < prob):
            index = int(random.random()*len(x))
            x[index] = 1-x[index]
    return x
    
def ga(Npop, crossProb, mutationProb):
    Ngen = 10
    minf = 99999
    
    ret = np.zeros((Ngen))
    retC = np.zeros((Ngen))
    
    x = starting_generation(Npop)
    for i in range(Ngen):
        f = function(x)
        if np.min(f) < minf:
            minf = np.min(f)
        #print(i , 'th generation min: ' , minf)
        ret[i] = np.min(f)
        retC[i] = minf
        parents = selection(x, f, int(Npop-Npop/5))
        next_x = crossing(parents, crossProb, Npop)
        next_x = mutation(next_x, mutationProb)
        
        for j in range(len(parents)):
            x[j] = parents[j]
        for j in range(len(next_x)):
            x[len(parents) + j] = next_x[j]
    return ret, retC


plt.figure()
res = np.zeros((20, 10))
resC = np.zeros((20, 10))
for i in range(20):
    res[i], resC[i] = ga(100, 0.8, 0.1)
    plt.plot(np.arange(0, 10, 1), res[i])
    
cMin = np.sum(res, axis=0) / 20
plt.figure()
plt.plot(np.arange(0,10,1), cMin)
