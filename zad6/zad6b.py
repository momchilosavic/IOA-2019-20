import math
import scipy.optimize as opt
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

Rc = 1000
Re = 1000

E = 5
Vcc = 12
Vt = 0.026

Is = 0.0000000000001

BetaF = 100
BetaR = 2

E = np.arange(0,10.1,0.1)
IB = np.empty((len(E)))
IC = np.empty((len(E)))
IE = np.empty((len(E)))
VBC = np.empty((len(E)))
VBE = np.empty((len(E)))
VCE = np.empty((len(E)))
COST = np.empty((len(E)))


#############################

def cost(x):
    Vbc, Vbe = x
    iB = Is * (1/BetaF * (math.exp(Vbe/Vt) - 1) - 1/BetaR * (math.exp(Vbc/Vt) - 1))
    iC = Is * ((math.exp(Vbe/Vt) - math.exp(Vbc/Vt)) - 1/BetaR * (math.exp(Vbc/Vt) - 1))
    iE = iB + iC
    E = Vbe + Re*iE
    return (abs(E - Vbe - Re*iE) + abs(Vcc - Rc*iC + Vbc - E))
    
    
#############################

X = np.linspace(-12, 0, 100)
Y = np.arange(-0.1, 0.6, 100)
X, Y = np.meshgrid(X, Y)
Z = np.empty((len(X), len(X[0])))
for i in range(len(X)):
    for j in range(len(X[0])):
        Z[i][j] = cost([X[i][j], Y[i][j]])
        
fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, \
                       linewidth=0, antialiased=False, alpha=0.5)
#fig.colorbar(surf, shrink=0.5, aspect=5)
#color = "b"
#ax.view_init(30, 45)

