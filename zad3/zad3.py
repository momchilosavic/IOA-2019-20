import numpy as np
import matplotlib.pyplot as plt
import time

x=[]

x.append([62.0, 58.4])
x.append([57.5, 56.0])
x.append([51.7, 56.0])
x.append([67.9, 19.6])
x.append([57.7, 42.1])
x.append([54.2, 29.1])
x.append([46.0, 45.1])
x.append([34.7, 45.1])
x.append([45.7, 25.1])
x.append([34.7, 26.4])
x.append([28.4, 31.7])
x.append([33.4, 60.5])
x.append([22.9, 32.7])
x.append([21.5, 45.8])
x.append([15.3, 37.8])
x.append([15.1, 49.6])
x.append([9.1, 52.8])
x.append([9.1, 40.3])
x.append([2.7, 56.8])
x.append([2.7, 33.1])

x = np.array(x)

# Calculate the euclidian distance in n-space of the route r traversing holes c, ending at the path start.
path_distance = lambda r,h: np.sum([np.linalg.norm(h[r[p]]-h[r[p-1]]) for p in range(len(r))])

# Reverse the order of all elements from element i to element k in array r.
two_opt_swap = lambda r,i,k: np.concatenate((r[0:i],r[k:-len(r)+i-1:-1],r[k+1:len(r)]))


########## TWO OPT ALGORITHM #####
def two_opt(holes,improvement_threshold):
    route = np.arange(holes.shape[0])
    improvement_factor = 1 # Initialize the improvement factor.
    best_distance = path_distance(route,holes) # Calculate the distance of the initial path.
    while improvement_factor > improvement_threshold: # If the route is still improving, keep going!
        distance_to_beat = best_distance # Record the distance at the beginning of the loop.
        for swap_first in range(1,len(route)-1):
            for swap_last in range(swap_first+1,len(route)):
                new_route = two_opt_swap(route,swap_first,swap_last)
                new_distance = path_distance(new_route,holes)
                if new_distance < best_distance:
                    route = new_route
                    best_distance = new_distance
        improvement_factor = 1 - best_distance/distance_to_beat # Calculate how much the route has improved.
    return route 


########## THREE OPT ALGORITHM #####
def three_opt(holes,improvement_threshold): # 2-opt Algorithm adapted from https://en.wikipedia.org/wiki/2-opt
    route = np.arange(holes.shape[0]) # Make an array of row numbers corresponding to cities.
    improvement_factor = 1 # Initialize the improvement factor.
    best_distance = path_distance(route,holes) # Calculate the distance of the initial path.
    while improvement_factor > improvement_threshold: # If the route is still improving, keep going!
        distance_to_beat = best_distance # Record the distance at the beginning of the loop.
        for swap_first in range(1,len(route)-2):
            for swap_last in range(swap_first+1,len(route)-1):
                for swap_mid in range(swap_last + 1, len(route)):
                    for cnt in range(4):
                        if cnt % 2 == 0:
                            new_route = two_opt_swap(route,swap_first,swap_last) 
                        else:
                            new_route = two_opt_swap(route,swap_last,swap_mid)
                        new_distance = path_distance(new_route,holes)
                        if new_distance < best_distance:
                            route = new_route
                            best_distance = new_distance
        improvement_factor = 1 - best_distance/distance_to_beat # Calculate how much the route has improved.
    return route 


########## FOUR OPT ALGORITHM #####
def four_opt(holes,improvement_threshold):
    route = np.arange(holes.shape[0])
    improvement_factor = 1 # Initialize the improvement factor.
    best_distance = path_distance(route,holes) # Calculate the distance of the initial path.
    while improvement_factor > improvement_threshold: # If the route is still improving, keep going!
        distance_to_beat = best_distance # Record the distance at the beginning of the loop.
        for swap_first in range(1,len(route)-3):
            for swap_last in range(swap_first+1,len(route)-2):
                for swap_mid in range(swap_last + 1, len(route) - 1):
                    for swap_fourth in range(swap_mid + 1, len(route)):
                        for cnt in range(22):
                            if cnt == 5:
                                new_route = two_opt_swap(route, swap_first, swap_last)
                            if cnt == 11:
                                new_route = two_opt_swap(route, swap_first, swap_mid)
                            if cnt == 17:
                                new_route = two_opt_swap(route, swap_first, swap_fourth)
                            if cnt % 2 == 0:
                                new_route = two_opt_swap(route,swap_mid,swap_fourth)
                            else:
                                new_route = two_opt_swap(route,swap_last,swap_mid)
                            new_distance = path_distance(new_route,holes)
                            if new_distance < best_distance:
                                route = new_route
                                best_distance = new_distance
        improvement_factor = 1 - best_distance/distance_to_beat # Calculate how much the route has improved.
    return route
    

########## MAIN #####
mov = 0
start_time = time.time()
route = two_opt(np.roll(x, mov, axis=0), 0.0001)
elapsed_time = time.time() - start_time

########## PLOT #####
new_holes_order = np.ndarray((len(route), 2))
#new_holes_order = np.concatenate((np.array([x[route[i]] for i in range(len(route))]),np.array([x[0]])))
for i in range(len(route)):
    new_holes_order[i] = x[route[i]]
plt.scatter(x[:,0],x[:,1])
plt.plot(new_holes_order[:,0],new_holes_order[:,1], 'r')
plt.show()
########## PRINT STATS #####
print("\nRoute: " + str((route + mov) % 20 + 1) + "\nDistance: " + str(path_distance(route,x)))
print("Time elapsed: ", elapsed_time)