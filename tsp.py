import random
import time
import math

from input_output import read_input, write_output
from town import Town, Individual, Population
from genetic_algo_utils import crossover_and_mutate_population, generate_initial_population, get_next_population_and_best_individual

DEBUG = True

def get_generations(num_cities: int) -> int:
    """
    Exponential decay function to determine number of generations based on number of cities.
    Starts at 100 generations for upto 100 cities, and exponentially approaches 10 generations
    """
    if num_cities < 100:
        return 100

    # Parameters for decay function
    A = 150   # Starting amplitude
    B = 0.015  # Decay speed, keep it high
    C = 10    # Asymptotic floor at 10 generations for large city counts

    # Calculate generations using the exponential decay formula
    gens = int(max(C, A * math.exp(-B * (num_cities - 100)) + C))

    return gens


def run():
    # To make results consistent
    random.seed(42)

    # Read input and create Town object
    cities = read_input()
    town = Town(cities)

    # Create initial population
    population_size = 1000
    town.population = generate_initial_population(
        population_size, town.number_of_cities)

    # Initialize variables to track the best solution
    best_individual: Individual = []
    min_cost = float('inf')
    prev_min_cost = float('inf')

    # Determine number of generations based on number of cities
    number_of_generations = get_generations(town.number_of_cities)

    # Counter to track subsequent generations without improvement
    stagnation_count = 0
    # Stop the loop if the counter exceeds this threshold
    max_no_improvement_generations = 20
    # Increase mutation rate if no improvement for these many generations
    base_mutation_rate = 0.01
    max_mutation_rate = 0.03
    mutation_rate = base_mutation_rate
    max_stagnation_count = max_no_improvement_generations/2


    if DEBUG:
        print(f"Number of generations set to: {number_of_generations} for {town.number_of_cities} cities")
        run_loop_start_time = time.time()

    # Create a loop for each generation
    for generation in range(number_of_generations):
        # Get next population and best individual in current population
        town.population, new_best_individual, new_min_cost = get_next_population_and_best_individual(
            town, generation, min_tournament_size=5, max_tournament_size=9)

        # if DEBUG:
        # print("Population size after selection:", len(town.population))

        # Update best individual and cost if improved
        if new_min_cost < min_cost:
            min_cost = new_min_cost
            best_individual = new_best_individual

        # Update stagnation counter
        if new_min_cost < prev_min_cost:
            prev_min_cost = new_min_cost
            stagnation_count = 0
        else:
            stagnation_count += 1
            if stagnation_count > max_no_improvement_generations:
                break

        # Adjust mutation rate based on stagnation
        if stagnation_count > max_stagnation_count:
            mutation_rate = max(1.5*mutation_rate, max_mutation_rate)
        else:
            mutation_rate = base_mutation_rate

        # Crossover and Mutation
        town.population = crossover_and_mutate_population(
            town, mutation_rate=mutation_rate)
        # if DEBUG:
        # print("Population size after crossover and mutation:", len(town.population))

        if DEBUG:
            if generation % 10 == 0:
                end_time = time.time()
                print(
                    f"{generation} Generation done. Time taken so far: {end_time - run_loop_start_time} seconds. Best cost: {min_cost}")

    if DEBUG:
        run_loop_end_time = time.time()
        print(f"Time taken: {run_loop_end_time - run_loop_start_time} seconds")
        print(f"Min cost {min_cost}")
    final_path = [town.city_map[i] for i in best_individual]
    final_path.append(town.city_map[best_individual[0]])
    write_output(min_cost, final_path)


if __name__ == "__main__":
    run()
