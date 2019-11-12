import math
import numpy as np
from scipy import optimize
from scipy.optimize import fsolve
from scipy.optimize import NonlinearConstraint
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

##### VARIABLES ############################################################################
Rc = 1000
Re = 1000

E = 5
Vcc = 12
Vt = 0.026

Is = 1.0e-13

BetaF = 100
BetaR = 2

E = np.arange(0, 10.1, 0.1)

VBE = np.empty((len(E)))
VBC = np.empty((len(E)))
VCE = np.empty((len(E)))
VOUT = np.empty((len(E)))

IB = np.empty((len(E)))
IC = np.empty((len(E)))
IE = np.empty((len(E)))

COST = np.empty((len(E)))
COSTE = np.empty((len(E), 3))
#############################################################################################

##### FUNCTIONS #############################################################################
def equations(x, E):
    iB, iC, iE, Vbc, Vbe = x
    funcs = np.empty((5))
    funcs[0] = iB - Is * (1/BetaF * (math.exp(Vbe/Vt) - 1) - \
         1/BetaR * (math.exp(Vbc/Vt) - 1))   # iB
    funcs[1] = iC - Is * ((math.exp(Vbe/Vt) - math.exp(Vbc/Vt)) - \
         1/BetaR * (math.exp(Vbc/Vt) - 1))   # iC
    funcs[2] = iE - iC - iB           # iE
    funcs[3] = E - Vbe - iE*Re         # Vbe
    funcs[4] = Vcc - E - iC*Rc + Vbc  # Vbc
    return funcs

def cost(x, Y, E):
    Vbc, Vbe = x
    iC, iE = Y
    return abs(E - Vbe - Re * iE) + abs(Vcc - Rc * iC + Vbc - E)

def costOptimization(x):
    Vbc, Vbe = x
    iB = Is * (1/BetaF * (math.exp(Vbe/Vt) - 1) - 1/BetaR * (math.exp(Vbc/Vt) - 1))
    iC = Is * ((math.exp(Vbe/Vt) - math.exp(Vbc/Vt)) - 1/BetaR * (math.exp(Vbc/Vt) - 1))
    iE = iB + iC
    E = Vbe + iE*Re
    return cost(x, [iC, iE], E)

#############################################################################################

##### NON-LINEAR SYSTEM CALCULATION #########################################################
for i in range(len(E)):
    res = least_squares(equations, (0,0,0,0,0), args = (E[i],), \
                        bounds=((0,0,0, -999,-999),(999,999,999,999,999)))
    IB[i], IC[i], IE[i], VBC[i], VBE[i] = res.x[0], res.x[1], res.x[2], res.x[3], res.x[4]
    VCE[i] = Vcc - IC[i]*Rc - IE[i]*Re
    VOUT[i] = Re * IE[i] + VCE[i]
    COST[i] = cost([VBC[i], VBE[i]], [IC[i], IE[i]], E[i])
print("")
print("f(min) = ", np.min(COST))
print("")
#############################################################################################

###### OPTIMIZATION #########################################################################
indexes = np.where(COST == np.min(COST))[0]
OPT = np.ndarray(len(indexes), dtype=optimize.optimize.OptimizeResult)
for i in range(len(indexes)):
    res = optimize.minimize(costOptimization, [VBC[indexes[i]], VBE[indexes[i]]], \
                            method = 'Nelder-Mead')
    OPT[i] = res

MINOPT = OPT[0]
MININD = indexes[0]
for i in range(1, len(OPT)):
    if(OPT[i].fun < MINOPT.fun):
        MINOPT = OPT[i]
        MININD = indexes[i]
print(MINOPT)
print("")
print("Vbc = ", VBC[MININD], "Vbe = ", VBE[MININD], "Vce = ", VCE[MININD], "iB = ", IB[MININD] \
      , "iC = ", IC[MININD], "iE = ", IE[MININD], "E = ", E[MININD])
#############################################################################################

##### COST FUNCTION PLOT ####################################################################
X, Y = np.meshgrid(VBC, VBE)
M, N = np.meshgrid(IC, IE)
Z = np.empty((len(E), len(E)))
for i in range(len(X)):
    for j in range(len(X[0])):
        Z[i][j] = cost([X[i][j], Y[i][j]], [M[i][j], N[i][j]], E[j])
        
fi = plt.figure()
ax = fi.gca(projection = '3d')
j = ax.plot_surface(X,Y,Z,cmap=plt.cm.viridis, linewidth=0.2)
ax.view_init(15, 45)
ax.set_xlabel('VBE')
ax.set_ylabel('VBC')
a = np.where(Z == np.min(Z))[0]
b = np.where(Z == np.min(Z))[1]
for i in range(len(a)):
    ax.scatter(X[a[i]][b[i]], Y[a[i]][b[i]], Z[a[i]][b[i]])
plt.show()
##############################################################################################

##### PLOTS ##################################################################################
plt.figure()
plt.plot(E, VBE, label='Vbe(E)')
plt.grid(True)
plt.legend(loc='lower center', ncol=1)

plt.figure()
plt.plot(E, IC, label='iC(E)')
plt.grid(True)
plt.legend(loc='lower center', ncol=1)

plt.figure()
plt.plot(E, VOUT, label='Vout(E)')
plt.grid(True)
plt.legend(loc='lower center', ncol=1)
##############################################################################################