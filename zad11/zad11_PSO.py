import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

def dist(A, B):
    sum = 0
    for i in range(len(A)):
        sum += math.pow(A[i]-B[i], 2)
    return math.sqrt(sum)

def opt(x):
    S1 = np.array(x[:3])
    S2 = np.array(x[3:])
    A, B, C, D = np.array([[1, 5, 1], [3, 2, 0], [5, 6, 1], [6, 3, 3]])
    return dist(A, S1) + dist(B, S1) + dist(S1, S2) + dist(C, S2) + dist(D, S2)

###############################################################################

#Some variables to calculate the velocity
W = 0.729
c1 = 1.494
c2 = 1.494
target = 1

n_iterations = 100
target_error = 0.0001
n_particles = 50
D = 6
particle_position_vector = np.zeros((n_particles, D))
for i in range(n_particles):
    particle_position_vector[i] = np.array([np.random.randint(10, size=D)])
    
pbest_position = particle_position_vector
pbest_fitness_value = np.array([float('inf') for _ in range(n_particles)])
gbest_fitness_value = float('inf')
gbest_position = np.array([float('inf'), float('inf')])

velocity_vector = ([np.array([0]*D) for _ in range(n_particles)])
iteration = 0
while iteration < n_iterations:
    for i in range(n_particles):
        fitness_cadidate = opt(particle_position_vector[i])
        #print(fitness_cadidate, ' ', particle_position_vector[i])
        
        if(pbest_fitness_value[i] > fitness_cadidate):
            pbest_fitness_value[i] = fitness_cadidate
            pbest_position[i] = particle_position_vector[i]

        if(gbest_fitness_value > fitness_cadidate):
            gbest_fitness_value = fitness_cadidate
            gbest_position = particle_position_vector[i]

    if(abs(gbest_fitness_value - target) < target_error):
        break
    
    for i in range(n_particles):
        new_velocity = (W*velocity_vector[i]) + (c1*random.random()) * (pbest_position[i] - particle_position_vector[i]) + (c2*random.random()) * (gbest_position-particle_position_vector[i])
        new_position = new_velocity + particle_position_vector[i]
        particle_position_vector[i] = new_position

    iteration = iteration + 1
    
print("The best position is ", gbest_position)
print("fmin ", gbest_fitness_value)
print("in iteration number ", iteration)
    

#################
A, B, C, D = np.array([[1, 5, 1], [3, 2, 0], [5, 6, 1], [6, 3, 3]])
S1 = np.array(gbest_position[:3])
S2 = np.array(gbest_position[3:])

fig = plt.figure(figsize=((8,6)), dpi=80)
ax = fig.add_subplot(111, projection='3d')
ax.scatter(A[0], A[1], A[2])
ax.scatter(B[0], B[1], B[2])
ax.scatter(C[0], C[1], C[2])
ax.scatter(D[0], D[1], D[2])
ax.scatter(S1[0], S1[1], S1[2])
ax.scatter(S2[0], S2[1], S2[2])
plt.plot([A[0], S1[0]], [A[1],S1[1]], [A[2], S1[2]])
plt.plot([B[0], S1[0]], [B[1],S1[1]], [B[2], S1[2]])
plt.plot([S2[0], S1[0]], [S2[1],S1[1]], [S2[2], S1[2]])
plt.plot([C[0], S2[0]], [C[1],S2[1]], [C[2], S2[2]])
plt.plot([D[0], S2[0]], [D[1],S2[1]], [D[2], S2[2]])
#ax.view_init(45, 60)
plt.show()
