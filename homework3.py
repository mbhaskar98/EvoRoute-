import random
import time
import math

from input_output import read_input, write_output
from town import Town, Individual, Population
from genetic_algo_utils import crossover_and_mutate_population, generate_initial_population, get_next_population_and_best_individual

DEBUG = True


def run():
    # To make results consistent
    random.seed(42)

    # Read input and create Town object
    cities = read_input()
    town = Town(cities)

    # Create initial population
    # TODO: Adjust population based on problem size
    population_size = 1000
    town.population = generate_initial_population(
        population_size, town.number_of_cities)

    best_individual: Individual = []
    min_cost = float('inf')
    prev_min_cost = float('inf')


    delete_me_factor = 50

    base_generations = 200 - delete_me_factor
    number_of_generations = base_generations
    city_threshold = 150 - delete_me_factor
    min_generations = 75 - delete_me_factor
    decay_rate = 5

    if len(cities) > city_threshold:
        # Apply logarithmic decay to reduce generations for larger cities
        # Generations = base - log(n - threshold + 1) * decay_rate
        decay = math.log(len(cities) - city_threshold + 1)
        number_of_generations = int(
            max(min_generations, base_generations - decay * decay_rate))
    else:
        number_of_generations = base_generations


    stangnation_count = 0
    # Stop the loop if the counter exceeds this threshold
    max_no_improvement_generations = 20
    # Increase mutation rate if no improvement for these many generations
    base_mutation_rate = 0.01
    mutation_rate = base_mutation_rate
    max_stagnation_count = max_no_improvement_generations/2

    if DEBUG:
        print(f"Number of generations set to: {number_of_generations}")
        run_loop_start_time = time.time()

    # Create a loop for each generation
    for generation in range(number_of_generations):
        # Get next population and best individual in current population
        k_min = 5
        k_max = 9
        alpha = 0.05
        tournament_size = min(k_max, k_min + alpha * generation)
        town.population, new_best_individual, new_min_cost = get_next_population_and_best_individual(
            town, tournament_size=int(tournament_size))

        # if DEBUG:
        # print("Population size after selection:", len(town.population))

        if new_min_cost < min_cost:
            min_cost = new_min_cost
            best_individual = new_best_individual

        if new_min_cost < prev_min_cost:
            prev_min_cost = new_min_cost
            stangnation_count = 0
        else:
            stangnation_count += 1
            if stangnation_count > max_no_improvement_generations:
                break

        if stangnation_count > max_stagnation_count:
            mutation_rate *= 1.5
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