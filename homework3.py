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
    population_size = 20000
    town.population = generate_initial_population(population_size, town.number_of_cities)

    best_individual : Individual = []
    min_cost = float('inf')

    # Create a loop for each generation
    # TODO: Adjust number of generations based on problem size
    number_of_generations = 100

    i = 0

    run_loop_start_time = time.time()
    for _ in range(number_of_generations):
        # Get next population and best individual in current population
        start_time = time.time()
        town.population, new_best_individual, new_min_cost = get_next_population_and_best_individual(town)
        end_time = time.time()

        if _ % 10 == 0:
            print(f"Time taken for selection: {end_time - start_time} seconds")

        if new_min_cost < min_cost:
            i = 0
            min_cost = new_min_cost
            best_individual = new_best_individual
        else:
            i += 1
            if i > 100:
                break

        start_time = time.time()
        # Crossover and Mutation
        town.population = crossover_and_mutate_population(town, mutation_rate=0.01)
        end_time = time.time()

        if _ % 10 == 0:
            print(f"Time taken for crossover and mutation: {end_time - start_time} seconds")

        if _ % 10 == 0:
            print(f"Generation {_} done. Best cost so far {min_cost}")
    run_loop_end_time = time.time()
    print(f"Time taken: {run_loop_end_time - run_loop_start_time} seconds")
    final_path = [town.city_map[i] for i in best_individual]
    final_path.append(town.city_map[best_individual[0]])
    print(f"Min cost {min_cost}")
    write_output(min_cost, final_path)

    
if __name__ == "__main__":
    run()