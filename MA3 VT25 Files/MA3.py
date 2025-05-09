""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc

def approximate_pi(n): # Ex1
    count = 0
    for i in range(n):
        value_1 = random.randint(0,100000) / 100000
        value_2 = random.randint(0,100000) / 100000
        if value_1 ** 2 + value_2 ** 2 <= 1:
             count += 1
    
    return 4 * count / n


def sphere_volume(n, d): # Ex2
    points = []
    for _ in range(n):  # Repeat n times to create n points
        point = (map(lambda x: random.uniform(-1, 1), range(d)))  # Create a point with d random numbers
        points.append(point)  # Add the point to the list

    # Use map to compute the squared distance from origin
    distances = list(map(lambda point: sum(map(lambda x: x**2, point)), points))

    # Filter the points that are inside the unit hypersphere
    inside_sphere = list(filter(lambda r2: r2 <= 1, distances))

    # The volume of the cube is 2^d, so the estimated volume is:
    volume_estimate = (len(inside_sphere) / n) * (2 ** d)
    return volume_estimate


def hypersphere_exact(d): #Ex2, real value 
    return m.pi ** (d / 2) / m.gamma(d / 2 + 1)

#Ex3: parallel code - parallelize for loop
hs_list = []
time_list = []
for i in range (10):
    hs_list.append(sphere_volume(100000, 11))
    time_list.append(pc())

def sphere_volume_parallel1(n, d, np=10):
    with future.ProcessPoolExecutor(max_workers=np) as executor:
        futures = [executor.submit(sphere_volume, n, d) for i in range(np)]
        results = ([f.result() for f in futures])
    return sum(results) / len(results)

#Ex4: parallel code - parallelize actual computations by splitting data
n = 10**6
d = 11

start = pc()
volume = sphere_volume(n, d)
end = pc()

print(f"Estimated volume of {d}-dimensional unit hypersphere with n={n}: {volume:.6f}")
print(f"Elapsed time: {end - start:.2f} seconds")

def count_inside_sphere(n_chunk, d):
    points = [list(random.uniform(-1, 1) for _ in range(d)) for _ in range(n_chunk)]
    distances = []
    for i in range (n_chunk):
        distances.append(sum(points[i]))
    return sum(1 for r2 in distances if r2 <= 1)


# Parallel version of sphere_volume
def sphere_volume_parallel2(n, d, np=10):
    chunk_size = n // np
    remainder = n % np
    start = pc()
    with future.ProcessPoolExecutor(max_workers=np) as executor:
        futures = [executor.submit(count_inside_sphere, chunk_size, d) for _ in range(np)]        
        total_inside = sum([f.result() for f in futures])
        if remainder > 0:
            total_inside += count_inside_sphere(remainder, d)
    end = pc()
    volume_estimate = (total_inside / n) * (2 ** d)
    return volume_estimate

def main():
    #Ex1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)

    #Ex2
    n = 100000
    d = 2
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    n = 100000
    d = 11
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    #Ex3
    n = 100000
    d = 11
    start = pc()
    for y in range (10):
        sphere_volume(n,d)
    stop = pc()
    total_time = stop - start
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")

    #Ex4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n,d)
    stop = pc()
    elapsed = stop - start
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")

if __name__ == '__main__':
	main()
#print(time_list)
#print(sum(hs_list) / (len(hs_list)))