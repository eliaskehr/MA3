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
    for _ in range(n):
        point = (map(lambda x: random.uniform(-1, 1), range(d)))
        points.append(point)

    distances = list(map(lambda point: sum(map(lambda x: x**2, point)), points))
    inside_sphere = list(filter(lambda r2: r2 <= 1, distances))
    volume_estimate = (len(inside_sphere) / n) * (2 ** d)
    return volume_estimate


def hypersphere_exact(d): #Ex2, real value 
    return m.pi ** (d / 2) / m.gamma(d / 2 + 1)

#Ex3:

def sphere_volume_parallel1(n, d, np=10):
    with future.ProcessPoolExecutor(max_workers=np) as executor:
        futures = [executor.submit(sphere_volume, n, d) for i in range(np)]
        results = ([f.result() for f in futures])
    return sum(results) / len(results)

#Ex4: parallel code - parallelize actual computations by splitting data

def count_inside_sphere(n, d):
    points = [list(random.uniform(-1, 1) for _ in range(d)) for _ in range(n)]
    count_tot = sum(1 for point in points if sum(x ** 2 for x in point) <= 1)
    return count_tot

# Parallel version of sphere_volume
def sphere_volume_parallel2(n, d, np=10):
    chunk_size = n // np
    remainder = n % np

    with future.ProcessPoolExecutor(max_workers=np) as executor:
        futures = [executor.submit(count_inside_sphere, chunk_size, d) for _ in range(np)]        
        total_inside = sum(f.result() for f in futures)
        if remainder > 0:
            total_inside += count_inside_sphere(remainder, d)

    volume_estimate = (total_inside / n) * (2 ** d)
    return volume_estimate

def main():
    #Ex1
    dots = [1000, 10000, 100000]
    for n in dots:
        value = approximate_pi(n)
    print(f"Approximate value of pi = {value}")

    #Ex2
    n = 100000
    d = 2
    #sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    n = 100000
    d = 11
    #sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    #Ex3
    n = 100000
    d = 11
    # Sequential version
    start = pc()
    for y in range (10):
        sphere_volume(n,d)
    stop = pc()
    total_time = stop - start
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")

    # Parallel version
    start = pc()
    #sphere_volume_parallel1(n,d)
    stop = pc()
    print(f"Ex3: Parallel time of {d} and {n}: {stop-start}")


    #Ex4
    n = 1000000
    d = 11
    start = pc()
    #sphere_volume(n,d)
    stop = pc()
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")

    print()
    print()
    print(sphere_volume_parallel1(n,d))
    print(sphere_volume_parallel2(n,d))
    print()

if __name__ == '__main__':
	main()   

