import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import math

##### READ DATA ##########
file = open('complex.txt', 'r')
delta = []
f = []
for line in file:
    s = line.split()
    if(len(s) != 0):
        delta.append(float(s[0]))
        f.append(float(s[1]))
file.close()

##### DRAW PLOT ##########
plt.figure()
plt.grid(b = 'true')
plt.plot(delta, f)
plt.xlabel('delta')
plt.ylabel('|F(delta)|')

##### DEFINE FUNCTION ##########
def fun(params, constants):
    delta = params[0]
    n, beta, d, teta = constants
    sum = [0, 0]
    fi = delta + d * beta * math.cos(teta)
    for k in range(int(n)):
        sum[0] = sum[0] + math.cos((-k) * fi)
        sum[1] = sum[1] + math.sin((-k) * fi)
    return math.sqrt(sum[0]**2 + sum[1]**2)

##### MINIMIZE FUNCTION ##########
constants = [5, 20*math.pi, 0.05, math.pi/4]
init_guess = [4]
res = minimize(lambda p,c: -fun(p,c), init_guess, args = constants, method='Nelder-Mead', options={'ftol': 1e-8, 'disp': True, 'maxfev': 1e4})
xmin = np.array(res.x)
print("max = ", xmin[0])

##### DRAW MAXIMUM ##########
plt.scatter(xmin[0], fun([xmin[0]], constants), facecolor='red')