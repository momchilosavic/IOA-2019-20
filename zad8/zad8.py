import numpy as np
import math
import matplotlib.pyplot as plt
from scipy import optimize

##### VARIABLS ################################################################
a = 0.95
T0 = 50
N = 100
iTot = 200
M = 20
###############################################################################

##### FUNCTIONS ###############################################################
def opt(x):
    sum = 0
    for i in range(len(x)):
        sum += x[i]
    return round(sum)

def nextTemp(T, a):
    return a*T

def hamming_distance(a, b):
    return sum(ch1 != ch2 for ch1, ch2 in zip(a, b))

XX = np.empty((100))
YY = np.empty((100))
ee = 0

def func(T0, a, iTot):
    rArr = np.zeros((iTot))
    T = T0
    e = iTot
    x = np.random.choice([0,1], size=(N,), p=[(iTot-e)/iTot,e/iTot])
    f = opt(x)
    while(e > 0):
        rArr[iTot - e] = f
        eTemp = e
        xTemp = x
        while(eTemp >= e):
            xTemp = np.random.choice([0,1], size=(N,), p=[(iTot-e)/iTot,e/iTot])
            eTemp = hamming_distance(x, xTemp)
        e -= 1      
        fTemp = opt(xTemp)
        
        if(fTemp < f):
            x = xTemp
            f=fTemp
        else:
            if(round(math.exp(-(opt(xTemp) - opt(x)) / T), 0) == 1):
                x = xTemp       
                f = fTemp
        if(e > 0):
            T = nextTemp(T, a)
    return rArr
###############################################################################
    
##### MAIN ####################################################################
plt.figure()
x = np.arange(0, iTot, 1)
r = np.zeros((M, iTot))
av = np.zeros((iTot))
for i in range(M):
    r[i] = func(T0, a, iTot)
    plt.plot(x, r[i])

plt.figure()
for i in range(M):
    for j in range(iTot):
        av[j] += r[i][j]
    
for i in range(iTot):
    av[i] /= M
plt.plot(x, av)
    
z = optimize.basinhopping(opt, x, niter=100, T=50, stepsize=1)