import numpy as np
import math
from scipy.optimize import minimize

########## PRINT #####
def printFunc(x):
    x1, x2, x3, x4 = x
    
    print("Prvi proizvod: ", round(x1/100,2))
    print("Drugi proizvod: ", round(x2/100,2))
    print("Treci proizvod: ", round(x3/100,2))
    print("Cetvrti proizvod: ", round(x4/100,2))


########## FUN #####
def func1(x, y):
    x1, x2, x3, x4 = x
    cnt = 0
    S = y * 100
    P = y * 100000000
    for i1 in range(len(x1)):
        for i2 in range(len(x2)):
            for i3 in range(len(x3)):
                for i4 in range(len(x4)):
                    cnt = cnt + 1
                    a = x1[i1]
                    b = x2[i2]
                    c = x3[i3]
                    d = x4[i4]
                    if a+b+c+d > S:
                        break
                    if a*b*c*d > P:
                        break
                    if a+b+c+d == S and a+b+c+d == P:
                        print("Iterations: ", cnt)
                        return [a, b, c, d]
    print("Iterations: ", cnt)
    return [-1, -1, -1, -1]
        
def func2(x, y):
    x1, x2, x3 = x
    x4 = 0
    cnt = 0
    S = y * 100
    P = y * 100000000
    for i1 in range(len(x1)):
        for i2 in range(len(x2)):
            for i3 in range(len(x3)):
                cnt = cnt + 1
                a = x1[i1]
                b = x2[i2]
                c = x3[i3]
                x4 = S - a - b - c
                if a*b*c*x4 > P:
                    break
                if a*b*c*x4 == P:
                    print("Iterations: ", cnt)
                    return [a, b, c, x4]
    print("Iterations: ", cnt)
    return [-1, -1, -1, -1]
        
def func3(y):
    fac = []
    cnt = 0
    S = round(y * 100)
    P = round(y * 100000000)
    for i in range(2, S):
        if P % i == 0:
            fac.append(i)
            
    for i1 in range(len(fac) - 3):
        for i2 in range(len(fac) - 2):
            for i3 in range(len(fac) - 1):
                for i4 in range(len(fac)):
                    cnt = cnt + 1
                    a = fac[i1]
                    b = fac[i2]
                    c = fac[i3]
                    d = fac[i4]
                    if a+b+c+d > S or a*b*c*d > P:
                        break
                    if a+b+c+d == S and a*b*c*d == P:
                        print("Iterantions: ", cnt)
                        return [a, b, c, d]
    print("Iterations: ", cnt)
    return[-1, -1, -1, -1]
    
                        


########## MAIN #####
x = np.arange(1, 711, 1)

#####
print("3rd soultion:")
rs = func3(7.11)
printFunc(rs)
print("")
print("")
#####
print("2nd solution:")
rs = func2([x, x, x], 7.11)
printFunc(rs)
print("")
print("")
#####
print("1st solution:")
rs = func1([x, x, x, x], 7.11)
printFunc(rs)
print("")
print("")

