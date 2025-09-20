from typing import List

from city import City


Individual = List[int]
Population = List[Individual]

class Town:
    def __init__(self, cities: List[City]):
        self.population : Population = []
        self.city_map = {}
        for i, city in enumerate(cities):
            self.city_map[i] = city
        self.number_of_cities = len(cities)
        number_of_cities = self.number_of_cities
        self.distance_between_cities = [[0] * number_of_cities for _ in range(number_of_cities)]
        for i in range(number_of_cities):
            for j in range(i + 1, number_of_cities):
                distance = cities[i].distance(cities[j])
                self.distance_between_cities[i][j] = distance
                self.distance_between_cities[j][i] = distance
    
    def add_to_population(self, individual: Individual) -> None:
        self.population.append(individual)