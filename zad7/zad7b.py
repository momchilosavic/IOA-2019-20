import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt

##### OPTIMIZE METHOD #########################################################
S1 = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
S2 = [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]
S3 = [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0]
S4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]

C1 = [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
C2 = [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]
C3 = [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]

P1 = [480, 0, 0, 650, 0, 0, 580, 0, 0, 390, 0, 0]
P2 = [0, 480, 0, 0, 650, 0, 0, 580, 0, 0, 390, 0]
P3 = [0, 0, 480, 0, 0, 650, 0, 0, 580, 0, 0, 390]

A = [S1, S2, S3, S4, C1, C2, C3, P1, P2, P3]
b = [18, 15, 23, 12, 10, 16, 8, 6800, 8700, 5300]
c = [-310, -310, -310, -380, -380, -380, -350, -350, -350, -285, -285, -285]

bnd = (0, None)
bnds = [bnd, bnd, bnd, bnd, bnd, bnd, bnd, bnd, bnd, bnd, bnd, bnd]

res = opt.linprog(c, A_ub = A, b_ub = b, bounds=bnds, method='interior-point')

print(res)
print()
print('Ormar 1: ')
print('Server 1: ', round(res.x[0],2))
print('Server 2: ', round(res.x[3],2))
print('Server 3: ', round(res.x[6],2))
print('Server 4: ', round(res.x[9],2))
print('Ormar 2: ')
print('Server 1: ', round(res.x[1],2))
print('Server 2: ', round(res.x[4],2))
print('Server 3: ', round(res.x[7],2))
print('Server 4: ', round(res.x[10],2))
print('Ormar 3: ')
print('Server 1: ', round(res.x[2],2))
print('Server 2: ', round(res.x[5],2))
print('Server 3: ', round(res.x[8],2))
print('Server 4: ', round(res.x[11],2))
"""
print('\n')
print('Max capacity: ', ((res.x[0]+res.x[1]+res.x[2])*310 + \
                         (res.x[3]+res.x[4]+res.x[5])*380 + \
                         (res.x[6]+res.x[7]+res.x[8])*350 + \
                         (res.x[9]+res.x[10]+res.x[11])*285))
print('Ormar A: ', (res.x[0],res.x[3],res.x[6], res.x[9]))
print('Power A: ', (res.x[0]*480 + res.x[3]*650 + res.x[6]*580 + res.x[9]*390))
print('Ormar B: ', (res.x[1],res.x[4],res.x[7], res.x[10]))
print('Power B: ', (res.x[1]*480 + res.x[4]*650 + res.x[7]*580 + res.x[10]*390))
print('Ormar C: ', (res.x[2],res.x[5],res.x[8], res.x[11]))
print('Power C: ', (res.x[2]*480 + res.x[5]*650 + res.x[8]*580 + res.x[11]*390))
"""
###############################################################################

##### SIMPLEX IMPLEMENTATION ##################################################
    ##### FUNCTIONS ###########################################################
def matrixUpdate(_A, _b, row, column):
    A = np.copy(_A)
    b = np.copy(_b)
    for i in range(len(A)):
        if i != row:
            factor = -1
            if(A[row][column] == 0):
                continue;
            else:
                factor = factor/A[row][column]*A[i][column]
            for j in range(len(A[0])):
                A[i][j] += A[row][j] * factor
            b[i] += b[row] * factor
    return A, b

def findMaxValue(A, b, column):
    maxValue = 999999
    maxIndex = -1
    for i in range(1, len(A)):
        if(A[i][column] > 0 and b[i]/A[i][column] > 0 and b[i]/A[i][column] < maxValue):
            maxValue = b[i]/A[i][column]
            maxIndex = i
    return [maxValue, maxIndex]

def calculateCost(variables, values):
    cost = 0
    for i in range(len(variables)):
        cost += variables[i]*values[i]
    return cost

def updateVariables(A, b, variables, variableNumber):
    for i in range(1, len(A)):
        for j in range(len(variables)):
            if j != variableNumber and variables[j] > 0 and A[i][j+1] != 0:
                variables[j] = b[i] - variables[variableNumber]*A[i][variableNumber+1]
                variables[j] /= A[i][j+1]
    return variables

def function(_A, _b, varCount, VALUES):
    A = np.copy(_A)
    b = np.copy(_b)
    improvment = 1
    variables = np.zeros((varCount))
    cost = 1
    newCost = 1
    costToBeat = 1
    while(improvment > 0):
        costToBeat = cost
        for k in range(varCount):
            i = (k + 2) % varCount
            if(A[0][i+1] < 0):
                maxValue, maxIndex = findMaxValue(A, b, i+1)
                if(maxIndex >= 0):
                    variables[i] = maxValue
                    variables = updateVariables(A, b, variables, i)
                    newCost = calculateCost(variables, VALUES)
                    if(newCost > cost):
                        A, b = matrixUpdate(A, b, maxIndex, i+1)
                        cost = newCost
        improvment = 1 - costToBeat / cost
    return cost, variables
    ##### VARIABLES ###########################################################
Z = np.array([0., \
              -310, -310, -310,\
              -380, -380, -380,\
              -350, -350, -350,\
              -285, -285, -285,\
              0, 0, 0, 0,\
              0, 0, 0,\
              0, 0, 0])

S1 = np.array([0.,\
               1, 1, 1,\
               0, 0, 0,\
               0, 0, 0,\
               0, 0, 0,\
               1, 0, 0, 0,\
               0, 0, 0,\
               0, 0, 0])
S2 = np.array([0.,\
               0, 0, 0,\
               1, 1, 1,\
               0, 0, 0,\
               0, 0, 0,\
               0, 1, 0, 0,\
               0, 0, 0,\
               0, 0, 0])
S3 = np.array([0.,\
               0, 0, 0,\
               0, 0, 0,\
               1, 1, 1,\
               0, 0, 0,\
               0, 0, 1, 0,\
               0, 0, 0,\
               0, 0, 0])
S4 = np.array([0.,\
               0, 0, 0,\
               0, 0, 0,\
               0, 0, 0,\
               1, 1, 1,\
               0, 0, 0, 1,\
               0, 0, 0,\
               0, 0, 0])

C1 = np.array([0.,\
               1, 0, 0,\
               1, 0, 0,\
               1, 0, 0,\
               1, 0, 0,\
               0, 0, 0, 0,\
               1, 0, 0,\
               0, 0, 0])
C2 = np.array([0.,\
               0, 1, 0,\
               0, 1, 0,\
               0, 1, 0,\
               0, 1, 0,\
               0, 0, 0, 0,\
               0, 1, 0,\
               0, 0, 0])
C3 = np.array([0.,\
               0, 0, 1,\
               0, 0, 1,\
               0, 0, 1,\
               0, 0, 1,\
               0, 0, 0, 0,\
               0, 0, 1,\
               0, 0, 0])

P1 = np.array([0.,\
               480, 0, 0,\
               650, 0, 0,\
               580, 0, 0,\
               390, 0, 0,\
               0, 0, 0, 0,\
               0, 0, 0,
               1, 0, 0])
P2 = np.array([0.,\
               0, 480, 0,\
               0, 650, 0,\
               0, 580, 0,\
               0, 390, 0,\
               0, 0, 0, 0,\
               0, 0, 0,\
               0, 1, 0])
P3 = np.array([0.,\
               0, 0, 480,\
               0, 0, 650,\
               0, 0, 580,\
               0, 0, 390,\
               0, 0, 0, 0,\
               0, 0, 0,\
               0, 0, 1])

A = np.array([Z, S1, S2, S3, S4, C1, C2, C3, P1, P2, P3])
b = np.array([0.,\
              18, 15, 23, 12,\
              10, 16, 8,\
              6800, 8700, 5300])

VALUES = [310, 310, 310, 380, 380, 380, 350, 350, 350, 285, 285, 285]
    ##### MAIN ################################################################
cost, variables = function(A, b, 12, VALUES)
print()
print('Max capacity: ', cost)
print()
print('Ormar 1: ')
print('Server 1: ', round(variables[0],2))
print('Server 2: ', round(variables[3],2))
print('Server 3: ', round(variables[6],2))
print('Server 4: ', round(variables[9],2))
print('Ormar 2: ')
print('Server 1: ', round(variables[1],2))
print('Server 2: ', round(variables[4],2))
print('Server 3: ', round(variables[7],2))
print('Server 4: ', round(variables[10],2))
print('Ormar 3: ')
print('Server 1: ', round(variables[2],2))
print('Server 2: ', round(variables[5],2))
print('Server 3: ', round(variables[8],2))
print('Server 4: ', round(variables[11],2))
###############################################################################