import numpy as np
import math
import sys
import random

def initial_population(size, n_cities):
    popu = []
    for i in range(size):
        popu.append([int]*n_cities)
    row = [0]*n_cities
    for j in range(n_cities):
        row[j] = j
    for i in range(size):
        row = sorted(row, key=lambda x: random.random())        #sufle row in o(n*log2(n))
        for j in range(n_cities):
            popu[i][j] = row[j]
    return popu

def get_element(popu, i):
    if popu is None:
        return -1  # Or raise a custom exception
    return popu[i]

def distance_popu(popula, n_cities, distance):
    dist_path = 0.0
    city_distance = 0.0
    idi = 0
    idj = 0
    for i in range(n_cities):
        if i + 1 == n_cities:
            idi = get_element(popula, i)
            idj = get_element(popula, 0)
            dist_path += distance[idi][idj]
        else:
            idi = get_element(popula, i)
            idj = get_element(popula, i+1)
            dist_path += distance[idi][idj]
    return dist_path

def fitness(popu, n_cities, distance):
    dist = float(distance_popu(popu, n_cities, distance))
    if(dist==0.0):
        return -1
    return (1/dist)

def select_parent_roulette(population, fitness_values):
    total_fitness = sum(fitness_values)
    id = 0
    sm = 0.0
    rd = np.random.rand() #% roletada
    if(total_fitness==0):
        return id
    for i in range(len(population)):
        porc = (fitness_values[i]/total_fitness)
        if(sm <rd and rd<=sm+porc):
            id = i
            break
        sm = sm + porc
    return population[id]

def crossover(parent1, parent2, n_cities, crossover_rate):
    if (random.random() < crossover_rate):
        point = random.randint(0, n_cities-2)
        list1 = [int]
        list2 = [int]
        for i in range(n_cities):
            if(i<=point):
                list1.append(get_element(parent2,i))
                list2.append(get_element(parent1,i))
            else:
                list1.append(get_element(parent1,i))
                list2.append(get_element(parent2,i))
        return list1, list2
    else:
        return parent1, parent2
        
def mutation(individual, n_cities, mutation_rate):
    
    for i in range(n_cities):
        if random.random() < mutation_rate:
            x = random.randint(0, n_cities-1)
            y = random.randint(0, n_cities-1)
            c = individual[x]
            individual[x] = individual[y]
            individual[y] = c

def genetic_algorithm(population_size, n_cities, generations,crossover_rate, mutation_rate):
    population = initial_population(population_size, n_cities)
    fitness_values = [0.0]*population_size
    print(fitness_values)
    for generation in range(generations):
        for i in range(len(population)):
            print(f'{len(population)} , {population_size}, {i} ')
            x = fitness(population[i], n_cities, distance)
            fitness_values[i] = x
            print(i)
        new_population = []
        for pp in range(population_size//2):
            parent1 = select_parent_roulette(population, fitness_values)
            parent2 = select_parent_roulette(population, fitness_values)
            offspring1 , offspring2 = crossover(parent1, parent2, n_cities, crossover_rate)
            new_population.extend([mutation(offspring1, n_cities, mutation_rate), mutation(offspring2, n_cities, mutation_rate)])
        
        population = new_population
        idc = 0
        for popu in population:
            fitness_values[idc] = fitness(popu, n_cities, distance)
            idc = idc + 1
        best_fitness = max(fitness_values)
        print(f'Generation {generation}: Best fitness = {best_fitness} ')
    index_best_fitness = fitness_values.index(max(fitness_values))
    best_population = population[index_best_fitness]
    print(f'Best Solution: {best_population}')
    print(f'Best Fitness: {fitness_values[index_best_fitness]}')
    print(f'Distance: {distance_popu(population[index_best_fitness], distance)}')

def calculate_distance(cities, distance, dimension):
    for i in range(dimension):
        for j in range(dimension):
            ca = cities[i]
            cb = cities[j]
            distance[i][j] = float(math.sqrt((cb[0]-ca[0])**2+(cb[1]-ca[1])**2))
            j = j + 1
        i = i + 1

if __name__== '__main__':
    #sys.stdin = open('wi29.tsp', 'r') 
    cities = []
    dimension = int(input())
    distance = []
    for i in range(dimension):
        distance.append([0.0]*dimension)
    for i in range(dimension) :
        msg = input()           #numero de cidades
        mg = msg.split()
        ct = int(mg[0])
        p1 = float(mg[1])            #ponto x
        p2 = float(mg[2])          #pont y
        point = p1, p2
        cities.append(point)
    calculate_distance(cities, distance, dimension)
    genetic_algorithm(25, dimension, 300,0.7, 0.01)


        
