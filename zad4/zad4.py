import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton
import math

def func(x, n):
    if(n < 2):
        return [x, 1]
    p = func(x, n-1)
    return [(2*n - 1)/n*x*p[0] - (n-1)/n*p[1], p[0]]

def funcD(x, n):
    return (n/(pow(x, 2)-1))*(x*func(x,n)[0]-func(x,n-1)[0])

R = 100
N = 10
x = np.linspace(-1, 1, R)

plt.figure()
plt.plot(x, func(x, N)[0], linewidth=0.75)
plt.plot(np.linspace(-1.2,1.2, R), np.linspace(0,0,R), 'r-', linewidth=0.5)
plt.xlim([-1.05,1.05])
for i in range(1, N+1):
    init_guess = math.cos(math.pi*(i-0.25)/(N+0.5))
    res = newton(lambda a, b: func(a,b)[0], init_guess, fprime = funcD, args=(N,), tol=1e-15)
    print("min(",i,") = ", res)
    plt.scatter(res, func(res, N)[0], facecolor="black", linewidths=1.5, marker='.')
    plt.text(res, -0.2*(i%2-0.5), ('x' + str(i)), fontsize=9)
plt.grid(True)
plt.show()



