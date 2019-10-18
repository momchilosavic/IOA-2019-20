import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

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

########## PARAM DFINITION #####
a = np.array([[-2, -2, -2, 0, 0, 0, 2, 2, 2],[2, 0, -2, 2, 0, -2, 2, 0, -2]])
c = np.array([0.02, 0.05, 0.09, 0.02, 0.05, 0.09, 0.02, 0.05, 0.09])
c=c*4
K = 10
M = len(c)

R = 50

Xmin    = -4
Xmax    =  4
Ymin    = -4
Ymax    =  4

x = np.arange(Xmin, Xmax, (Xmax-Xmin)/R)
y = np.arange(Ymin, Ymax, (Ymax-Ymin)/R)

x,y = np.meshgrid(x,y)
z = np.asarray(func([x, y], [a, c, K, M]))

########## PLOT #####
fi = plt.figure()
ax = fi.gca(projection = '3d')
j = ax.plot_surface(x,y,z,cmap=plt.cm.viridis, linewidth=0.2)
ax.view_init(30, 45)
plt.show()
