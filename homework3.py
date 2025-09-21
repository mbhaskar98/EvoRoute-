import random
import time

from input_output import read_input, write_output
from town import Town, Individual, Population
from genetic_algo_utils import crossover_and_mutate_population, generate_initial_population, get_next_population_and_best_individual

def run():
    # To make results consistent
    random.seed(42)
    
    # Read input and create Town object
    cities = read_input()
    town = Town(cities)
    
    # Create initial population
    # TODO: Adjust population based on problem size
    population_size = 4000
    town.population = generate_initial_population(population_size, town.number_of_cities)

    best_individual : Individual = []
    min_cost = float('inf')

    # Create a loop for each generation
    # TODO: Adjust number of generations based on problem size
    number_of_generations = 200

    i = 0

    run_loop_start_time = time.time()
    for _ in range(number_of_generations):
        # Get next population and best individual in current population
        town.population, new_best_individual, new_min_cost = get_next_population_and_best_individual(town)

        # print("Population size after selection:", len(town.population))

        if new_min_cost < min_cost:
            i = 0
            min_cost = new_min_cost
            best_individual = new_best_individual
        else:
            i += 1
            if i > 100:
                break

        # Crossover and Mutation
        town.population = crossover_and_mutate_population(town, mutation_rate=0.01)
        # print("Population size after crossover and mutation:", len(town.population))

        if _ % 10 == 0:
            end_time = time.time()
            print(f"{_} Generation done. Time taken so far: {end_time - run_loop_start_time} seconds. Best cost: {min_cost}")

    run_loop_end_time = time.time()
    print(f"Time taken: {run_loop_end_time - run_loop_start_time} seconds")
    final_path = [town.city_map[i] for i in best_individual]
    final_path.append(town.city_map[best_individual[0]])
    print(f"Min cost {min_cost}")
    write_output(min_cost, final_path)

    
if __name__ == "__main__":
    run()