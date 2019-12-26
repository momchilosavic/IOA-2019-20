import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy import optimize
import math

########## FUNCTION DEFINITION #####
def func(param, constants):
    x, y = param
    a, c, K, M = constants
    z = np.zeros((len(x[0]), len(y[0])))
    for i in range(len(x[0])):
        for j in range(len(y[0])):
        
            sum = 0
            for k in range(M):
                sum = sum + pow((   (np.matrix([x[i][j], y[i][j]]) - \
                                    np.matrix([a[0][k], a[1][k]]))*
                                    np.matrix.transpose(np.matrix([x[i][j], y[i][j]]) - \
                                                        np.matrix([a[0][k], a[1][k]])) + \
                                c[k]), -1)
            sum = K - sum
            z[i][j] = sum
    return z

def fun(param, constants):
    x = param
    a, c, K, M = constants
    
    sum = 0
    for i in range(M):
        sum = sum + pow(((np.matrix([x[0], x[1]]) - \
                                    np.matrix([a[0][i], a[1][i]]))*
                                    np.matrix.transpose(np.matrix([x[0], x[1]]) - \
                                                        np.matrix([a[0][i], a[1][i]])) + \
                                c[i]), -1)
    sum = K - sum
    return sum


######## PROB #####
def Q(N, k):
    if N == 1:
        return 1
    sum = 0
    for p in range(1, N):
        sum += math.factorial(N) / (math.factorial(p) * math.factorial(N-p)) * Q(p, k)
    return math.pow(N, k) - sum

def P(N, k):
    return Q(N, k)/math.pow(N, k)
########## PARAM DFINITION #####
a = np.array([[-3, -3, -3, 0, 0, 0, 3, 3, 3],[-3, 0, 3, -3, 0, 3, -3, 0, 3]])
c1 = np.array([0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2])
c2 = np.array([0.1, 0.2, 0.4, 0.2, 0.09, 0.21, 0.3, 0.1, 0.12])
K = 1
M = len(c1)
x = np.random.rand(2) * 8 - 4

######### OPTIMIZATION #####
W = 10                          ############################################### BROJ PONAVLJANJA
res = np.zeros((W, 2))
for i in range(W):
    x = np.random.rand(2) * 8 - 4
    r = optimize.minimize(fun, x, [a, c2, K, M], method = 'Nelder-Mead')
    res[i] = np.round(r.x, 0)

print('Verovatnoca za pronalazak 9 minimuma iz ', W, ' pokusaja: ', (P(9,W)))
print('Broj pronadjenih minimuma: ', np.unique(res, axis=0).size/2)
print('Minimumi: ')
for i in range(int(np.unique(res, axis=0).size/2)):
    print(np.unique(res, axis=0)[i])
