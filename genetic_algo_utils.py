
import random
import heapq
from typing import Tuple

from town import Town, Individual, Population


def generate_initial_population(pop_size: int, number_of_cities: int) -> Population:
    """
    Generate an initial population of individuals. 
    Each individual is a random permutation of city indices.
    """
    population: Population = []
    original_individual = list(range(number_of_cities))
    for _ in range(pop_size):
        individual = original_individual[:]
        random.shuffle(individual)
        population.append(individual)
    return population


def get_score_for_individual(individual: Individual, town: Town) -> float:
    # TODO: Optimize this function using memoization if needed
    """
    Calculate the total distance of the path represented by the individual.
    """

    total_distance = 0.0
    for i in range(len(individual)):
        # Add distance between current and previous city,
        # and between first and last city for a complete loop
        total_distance += town.distance_between_cities[individual[i]][individual[(i - 1)]]
    return total_distance


def get_next_population_and_best_individual(town: Town) -> Tuple[Population, Individual, float]:
    """
    Generate the next population.
    Find the best individual in the current population.
    Top 1% of individuals are carried over to the next generation.
    """
    new_population: Population = []
    new_population_indices = set()
    population_size = len(town.population)
    old_population = town.population

    # For adding randomness in selection.
    random.shuffle(old_population)
    
    # Elitism: Carry over the top x% individuals to the next generation
    top_x_percent_count = max(1, population_size // 1000)
    # top_x_percent_count = 10
    if top_x_percent_count % 2 != 0:
        # Even value for easy calculations
        top_x_percent_count += 1

    
    # Maintain a min-heap for the top 1% individuals
    # Python's heapq  min-heap, use negative score max-heap
    top_one_percent_individuals = []
    
    half_size = population_size // 2

    best_individual : Individual = None
    best_score = float('inf')

    for i in range(half_size):
        individual1_index = i
        individual2_index = i + half_size
        individual1 = old_population[individual1_index]
        individual2 = old_population[individual2_index]

        individual1_score = get_score_for_individual(individual1, town)
        individual2_score = get_score_for_individual(individual2, town)

        if individual1_score < best_score:
            best_score = individual1_score
            best_individual = individual1
        elif individual2_score < best_score:
            best_score = individual2_score
            best_individual = individual2


        # Add winner to the new population
        if individual1_score < individual2_score:
            new_population.append(individual1)
            new_population_indices.add(individual1_index)

            # Add other to 1% pool
            if len(top_one_percent_individuals) < top_x_percent_count:
                heapq.heappush(top_one_percent_individuals, (-individual2_score, individual2_index))
            elif individual2_score < -top_one_percent_individuals[0][0]:
                heapq.heapreplace(top_one_percent_individuals, (-individual2_score, individual2_index))
        else:
            new_population.append(individual2)
            new_population_indices.add(individual2_index)

            # Add other to 1% pool
            if len(top_one_percent_individuals) < top_x_percent_count:
                heapq.heappush(top_one_percent_individuals, (-individual1_score, individual1_index))
            elif individual1_score < -top_one_percent_individuals[0][0]:
                heapq.heapreplace(top_one_percent_individuals, (-individual1_score, individual1_index))
    
    # Add top 1% individuals to the new population
    for (_, index) in top_one_percent_individuals:
        if index not in new_population_indices:
            new_population.append(old_population[index])
            new_population_indices.add(index)

    if len(new_population) % 2 != 0:
        # Even value for easy calculations
        new_population.append(mutate_individual(old_population[0], 0.01))
        new_population_indices.add(0)


    return new_population, best_individual, best_score


def crossover_and_mutate_population(town: Town, mutation_rate : float = 0.01) -> Population:
    new_population: Population = []
    population_size = len(town.population)
    old_population = town.population

    half_size = population_size // 2

    for i in range(half_size):
        individual1 = old_population[i]
        individual2 = old_population[i + half_size]

    
        # Do it twice to maintain population size
        for _ in range(2):
            # Crossover
            new_individual1 = crossover_individuals(individual1, individual2)
            new_individual2 = crossover_individuals(individual2, individual1)
            
            if random.random() < mutation_rate:
                # Mutation
                new_individual1 = mutate_individual(new_individual1, mutation_rate)
            
            if random.random() < mutation_rate:
                # Mutation
                new_individual2 = mutate_individual(new_individual2, mutation_rate)

            new_population.append(new_individual1)
            new_population.append(new_individual2)

    return new_population

def crossover_individuals(individual1: Individual, individual2: Individual) -> Individual:
    """
    Perform ordered crossover between two individuals.
    """
    start = random.randint(0, len(individual1) - 1)
    end = random.randint(start, len(individual1) - 1)
    new_individual : Individual = []

    sub_array_from_individual1 = individual1[start:end]
    already_from_individual1 = set(sub_array_from_individual1)

    sub_array_from_individual2 = [city for city in individual2 if city not in already_from_individual1]

    for i in range(len(individual1)):
        if start <= i < end:
            new_individual.append(sub_array_from_individual1.pop(0))
        else:
            new_individual.append(sub_array_from_individual2.pop(0))

    return new_individual
        
    

def mutate_individual(individual: Individual, mutation_rate: float) -> Individual:
    """
    Mutate an individual by swapping two cities with a certain probability.
    """

    mutated_individual = individual[:]
    i, j = random.randint(0, len(individual) - 1), random.randint(0, len(individual) - 1)
    mutated_individual[i], mutated_individual[j] = mutated_individual[j], mutated_individual[i]
    return mutated_individual
