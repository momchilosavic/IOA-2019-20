import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt

##### OPTIMIZE METHOD #########################################################
A1 = [3, 1]
A2 = [1, 6]
A3 = [1, 3]

A = [A1, A2, A3]
b = [99, 288, 75]
c = [-20, -30]

x0_bounds = (0, None)
x1_bounds = (0, None)

res = opt.linprog(c, A_ub = A, b_ub = b, bounds=[x0_bounds, x1_bounds], method='simplex')

print(res)
print('\n')
print('Max profit: ', ((res.x[0])*20 + (res.x[1])*30),\
      'Count A: ', (res.x[0]), 'Count B: ', (res.x[1]))
###############################################################################


##### GRAPH METHOD ############################################################
    ##### VARIABLES ###########################################################
x = np.arange(0, 288, 1)    # x1
f1 = 99-3*x     # x2 = 99 - 3x1
f2 = (288-x)/6  # x2 = (288-x1)/6
f3 = (75-x)/3   # x2 = (75-x1)/3

    ##### PLOT FUNCTIONS ######################################################
plt.figure()

plt.plot(x, f1, label='3x1 + x2 <= 99')
plt.plot(x, f2, label='x1 + 6x2 <= 288')
plt.plot(x, f3, label='x1 + 3x2 <= 75')

plt.xlabel('x1')
plt.ylabel('x2')
plt.xlim((0, None))
plt.ylim((0, None))

plt.grid(True)
plt.legend()

    ##### FIND INTERSECTION POINTS ############################################
idx13 = np.argwhere(np.diff(np.sign(f3 - f1).flatten()))
    ##### PLOT INTERSECTION POINTS ############################################
plt.plot(x[idx13], f1[idx13], 'ro')
plt.plot(0, 0, 'ro')
plt.plot(x[0], f3[0], 'ro')

    ##### CALCULATE MAX PROFIT BASED ON INTERSECTION POINTS ###################
maxProfit = 0
maxCountA = 0
maxCountB = 0

aCount = [0, x[0], x[idx13[0][0]]]
bCount= [0, f3[0], f3[idx13[0][0]]]

for i in range(len(aCount)):
    if(aCount[i]*20 + bCount[i]*30 > maxProfit):
        maxProfit = aCount[i]*20 + bCount[i]*30
        countA = aCount[i]
        countB = bCount[i]
        
print('')
print('----- GRAPH METHOD -----')
print('')
print('Max profit: ', maxProfit)
print('A: ', countA)
print('B: ', countB)
print('Work hours: ', 3*countA + countB)
print('Chips used: ', countA + 6*countB)
print('Space used: ', countA + 3*countB)
###############################################################################

##### SIMPLEX IMPLEMENTATION ##################################################
    ##### VARIABLES ###########################################################
Z = np.array([0., -20, -30, 0, 0, 0])
A1 = np.array([0, 3, 1, 1, 0, 0])
A2 = np.array([0, 1, 6, 0, 1, 0])
A3 = np.array([0, 1, 3, 0, 0, 1])
A = np.array([Z, A1, A2, A3])
b = np.array([0., 99, 288, 75])

VALUES = [20, 30]
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

def function(A, b, varCount, Values):
    improvment = 1
    variables = np.zeros((varCount))
    cost = 1
    newCost = 1
    costToBeat = 1
    
    while(improvment > 0):
        costToBeat = cost
        for i in range(varCount):
            if(A[0][i+1] < 0):
                maxValue, maxIndex = findMaxValue(A, b, i+1)
                if(maxIndex >= 0):
                    variables[i] = maxValue
                    variables = updateVariables(A, b, variables, i)
                    newCost = calculateCost(variables, Values)
                    if(newCost > cost):
                        A, b = matrixUpdate(A, b, maxIndex, i+1)
                        cost = newCost
        improvment = 1 - costToBeat / cost
    print()
    print(cost)
    print(variables)
    return A, b
    ##### MAIN ################################################################
A, b = function(A, b, 2, VALUES)
###############################################################################

##### EXAMPLE #################################################################
"""
VALUES = [3, 2]
A2 = [[1,-3,-2,0,0,0], [0,1,1,1,0,0], [0,1,0,0,1,0], [0,0,1,0,0,1]]
B2 = [0,20,10,15]

A2, B2 = function(A2, B2, 2, VALUES)
"""
###############################################################################