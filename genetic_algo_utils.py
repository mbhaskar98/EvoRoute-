
import random
import heapq
from typing import Tuple
import time

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
        total_distance += town.distance_between_cities[individual[i]
                                                       ][individual[(i - 1)]]
    return total_distance


def get_next_population_and_best_individual(town: Town, number_of_generations: int, min_tournament_size: int = 3, max_tournament_size: int = 9) -> Tuple[Population, Individual, float]:
    """
    Generate the next population.
    Find the best individual in the current population using tournament selection.
    Tournament size increases with number of generations to balance exploration and exploitation.
    Top 1% of individuals are carried over to the next generation.
    This number of tournaments = (number_of_generations // 2).
    """

    alpha = 0.05
    tournament_size = int(min(max_tournament_size,
                          min_tournament_size + alpha * number_of_generations))

    # time_start = time.time()
    new_population: Population = []
    population_size = len(town.population)

    topk = int(0.05 * population_size)

    heap = []
    for individual in town.population:
        score = get_score_for_individual(individual, town)
        if len(heap) < topk:
            heapq.heappush(heap, (-score, individual))
        else:
            if score < -heap[0][0]:
                heapq.heappop(heap)
                heapq.heappush(heap, (-score, individual))

    for _ in range(((population_size)//2) - topk):
        tournament = random.sample(town.population, tournament_size)
        best_individual = min(
            tournament, key=lambda ind: get_score_for_individual(ind, town))
        new_population.append(best_individual)

    best_individual = min(
        new_population, key=lambda ind: get_score_for_individual(ind, town))
    best_score = get_score_for_individual(best_individual, town)
    for (_, individual) in heap:
        new_population.append(individual)
    # time_end = time.time()
    # print(f"Selection took {time_end - time_start} seconds")
    return new_population, best_individual, best_score


def crossover_and_mutate_population(town: Town, mutation_rate: float = 0.01) -> Population:
    """
    Do crossover and mutation to generate a new population.
    Applies 2-Opt refinement to 10% of the newly created individuals for local optimization to converge faster.
    """
    # start_time = time.time()
    new_population: Population = []
    population_size = len(town.population)
    old_population = town.population
    random.shuffle(old_population)

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
                new_individual1 = mutate_individual(
                    new_individual1, mutation_rate)
                if random.random() < 0.1:
                    # Apply 2-Opt to 10% of new children
                    new_individual1 = two_opt_refinement_fast(
                        new_individual1, town)

            if random.random() < mutation_rate:
                # Mutation
                new_individual2 = mutate_individual(
                    new_individual2, mutation_rate)
                if random.random() < 0.1:
                    # Apply 2-Opt to 10% of new children
                    new_individual2 = two_opt_refinement_fast(
                        new_individual2, town)
            new_population.append(new_individual1)
            new_population.append(new_individual2)

    # end_time = time.time()
    # print(f"Crossover and mutation took {end_time - start_time} seconds")

    return new_population


def crossover_individuals(individual1: Individual, individual2: Individual) -> Individual:
    """
    Perform ordered crossover between two individuals.
    """
    start = random.randint(0, len(individual1) - 1)
    end = random.randint(start, len(individual1) - 1)
    new_individual: Individual = []

    sub_array_from_individual1 = individual1[start:end]
    already_from_individual1 = set(sub_array_from_individual1)

    sub_array_from_individual2 = [
        city for city in individual2 if city not in already_from_individual1]

    for i in range(len(individual1)):
        if start <= i < end:
            new_individual.append(sub_array_from_individual1.pop(0))
        else:
            new_individual.append(sub_array_from_individual2.pop(0))

    return new_individual


def mutate_individual(individual: Individual, mutation_rate: float) -> Individual:
    """
    Mutate an individual by reversing a random sub-path.
    This mutation is more effective for TSP as it can significantly alter the path.
    """

    mutated_individual = individual[:]

    index_left = random.randint(0, len(mutated_individual) - 1)
    index_right = random.randint(0, len(mutated_individual) - 1)
    
    # Ensure index_left is less than index_right
    if index_left > index_right:
        index_left, index_right = index_right, index_left

    # Reverse the slice between index_left and index_right
    sub_path = mutated_individual[index_left:index_right+1]
    sub_path.reverse()
    mutated_individual[index_left:index_right+1] = sub_path

    return mutated_individual


def two_opt_refinement_fast(individual: Individual, town: Town) -> Individual:
    """
    Improves a given tour using a faster 2-Opt heuristic.
    It calculates the change in distance (delta) instead of re-calculating the entire tour length.
    """
    n = len(individual)
    best_individual = individual[:]
    dist_matrix = town.distance_between_cities

    improved = True
    while improved:
        improved = False
        for i in range(n - 2):
            for j in range(i + 2, n):
                # We are looking at edges (i, i+1) and (j, j+1 % n)
                # Let the four points be A, B, C, D
                A, B = best_individual[i], best_individual[i+1]
                C, D = best_individual[j], best_individual[(j+1) % n]

                # Current distance: dist(A,B) + dist(C,D)
                current_dist = dist_matrix[A][B] + dist_matrix[C][D]
                # New distance after swapping: dist(A,C) + dist(B,D)
                new_dist = dist_matrix[A][C] + dist_matrix[B][D]

                # If the new path is shorter, perform the swap by reversing the segment
                if new_dist < current_dist:
                    segment = best_individual[i+1: j+1]
                    segment.reverse()
                    best_individual[i+1: j+1] = segment

                    improved = True

    return best_individual
