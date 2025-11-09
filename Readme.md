# EvoRoute — Evolutionary Route Optimization (Genetic TSP Solver)

EvoRoute is an AI research/engineering project that applies evolutionary computation to the Traveling Salesman Problem (TSP). The repository contains a production-friendly, readable Python implementation of a genetic algorithm (GA) combined with local-search heuristics to quickly converge to high-quality routes.

---

## Highlights

- Simple, readable Python implementation suitable for learning and small experiments.
- Uses tournament selection, crossover and mutation operators to evolve routes.
- Includes a configurable population size and adaptive generation count.
- Designed as an AI/optimization project: reproducible experiments, tunable parameters, and local-search integrations.
- Uses tournament selection, crossover and mutation operators to evolve solutions, and integrates a 2-opt local-search heuristic to accelerate convergence and improve final tour quality.
- Includes a configurable population size and adaptive generation count.

## Prerequisites

- Python 3.7.5 or newer
- No external Python packages required (pure Python).

## Quick start

1.  Clone the repository:

        git clone https://github.com/mbhaskar98/TSP-genetic-algo.git
        cd TSP-genetic-algo

2.  Prepare an input file named `input.txt` in the project root. The expected input format is:

    - First line: n (number of cities)
    - Next n lines: three integers per line: x y z (coordinates or identifiers)

3.  Run the solver:

    python3 tsp.py

4.  After the run, results are written to `output.txt` with the minimum cost on the first line, followed by the chosen route (one city per line in the same x y z format).

## Input / Output specification (formal)

Input (file `input.txt`):

- 1st line: a strictly positive 32-bit integer N, the number of city locations.
- Next N lines: each line contains three non-negative 32-bit integers separated by a single space: `x y z` (the 3D grid coordinates of the city).

Output (file `output.txt`):

- 1st line: the computed total distance of the returned path (the program currently writes this as a floating point value).
- Next N+1 lines: each line contains three non-negative 32-bit integers separated by a single space: `x y z`. These lines list the cities in the order visited. The path ends at the start city, so the output lists N+1 coordinates (the first city repeated at the end).

Notes & example

- The program reads `input.txt` from the current working directory and writes `output.txt` to the same directory.
- Coordinates are written in the same integer format that was read.

Example (5 cities) — `input.txt`:

```
5
0 0 0
1 0 0
2 0 0
2 1 0
0 1 0
```

Corresponding valid `output.txt` (example) — note N+1 = 6 coordinate lines because the path returns to the start city:

```
12.0
0 0 0
1 0 0
2 0 0
2 1 0
0 1 0
0 0 0
```

The first line is the total distance for the tour; the following six lines are the visited city coordinates in order with the start repeated at the end.

## Files in this repository

- `tsp.py` — Main runner. Sets up the Town, population and runs the genetic algorithm loop.
- `town.py` — Town model and related classes (`Town`, `Individual`, `Population`). Contains distance calculations and structures used by the algorithm.
- `city.py` — `City` dataclass / object representing a city (x,y,z fields used for input/output and distance computation).
- `genetic_algo_utils.py` — Genetic algorithm building blocks: population generation, selection, crossover, mutation, and helper utilities.
- `input_output.py` — Simple I/O: `read_input()` reads `input.txt`; `write_output()` writes `output.txt` (format described above).

## Algorithm & parameters

The implementation uses these main components:

- Initial population: created randomly. The default population size in `tsp.py` is 1000.
- Selection: tournament selection (min and max tournament sizes configurable in `tsp.py`/`genetic_algo_utils.py`).
- Crossover & mutation: applied to create a new generation. Mutation rate can be adjusted and the runner adapts it if progress stalls.
- Stopping rules: number of generations is chosen by an exponential decay function based on the number of cities. The run also stops early when no improvement is observed for several generations.

### Optimizations & heuristics

- 2-opt local search: after crossover/mutation the implementation applies a 2-opt heuristic (a classical TSP edge-swap local optimization) to improve individuals — this significantly speeds convergence and raises final-quality solutions.
- Adaptive mutation: mutation rate increases when the population shows stagnation, helping escape local optima.
- Tournament selection with variable tournament sizes to balance selection pressure and diversity.

These are intended to demonstrate practical, research-oriented improvements over a naive GA.

Configuration knobs you may want to edit inside `tsp.py`:

- `population_size` — number of individuals in each generation (default 1000).
- `get_generations(num_cities)` — function that determines the number of generations. You can replace or tune its parameters.
- `base_mutation_rate`, `max_mutation_rate` — control mutation behavior when the search stagnates.

If you want to experiment, edit these values in `tsp.py` or implement a small CLI wrapper to pass them as arguments.

## Example

Given the example `input.txt` above, running `python3 tsp.py` will produce `output.txt` like:

```
<min_cost_float>
0 0 0
1 0 0
1 1 0
0 1 0
0 0 0
```

The first line is the total route cost; the following lines list the cities in the chosen visiting order and the route closes by returning to the starting city.

## Tips & notes

- For small numbers of cities (n < 10) the GA will often find optimal or near-optimal solutions quickly.
- For larger city sets, increase population size and generations for better results, but expect longer runtime.
- To reproduce runs, `tsp.py` seeds the RNG (`random.seed(42)`). Change/remove that if you want different random runs.
- This repository is presented as an AI project focused on evolutionary optimization and practical improvements (2-opt, adaptive mutation, selection tuning). Reworking parts of the GA (selection/crossover/mutation) or adding other local-search heuristics (3-opt, Lin–Kernighan) is encouraged for research experiments.

## Links for Reference
1. [Tutorials Point](https://www.tutorialspoint.com/genetic_algorithms/genetic_algorithms_parent_selection.htm#:~:text=selection%20are%20possible%20%E2%88%92-,Roulette%20Wheel%20Selection,-In%20a%20roulette)
2. [Tutorial-1](https://www.youtube.com/watch?v=uQj5UNhCPuo)
3. [Tutorial](https://www.youtube.com/watch?v=Wgn_aPH3OEk)
4. [Wlakthrough](https://medium.com/aimonks/traveling-salesman-problem-tsp-using-genetic-algorithm-fea640713758)


## Links for optimizations
1. [Reddit](https://www.reddit.com/r/Python/comments/k8c3jd/ive_made_a_genetic_algorithm_for_the_travelling/)
2. [Stack Overflow](https://stackoverflow.com/questions/47679966/how-can-i-improve-this-genetic-algorithm-for-the-tsp)
3. [Stack-Overflow (best optimization)](https://stackoverflow.com/questions/33597326/why-wont-my-genetic-algorithm-converge-or-at-least-get-a-little-better)


## Troubleshooting

- If `input.txt` is not found, create it in the project root with the expected format.
- If you see poor results, try increasing `population_size` or the number of generations.

## License

This project is licensed under the MIT License — see the `LICENSE` file for details.

Happy experimenting!
