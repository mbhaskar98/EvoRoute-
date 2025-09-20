from city import City
from typing import List


def read_input() -> List[City]:
    file = open("input.txt", "r")
    n = int(file.readline().strip())
    cities = []
    for _ in range(n):
        city = file.readline().strip()
        x, y, z = map(int, city.split())
        cities.append(City(x, y, z))
    return cities

def write_output(min_cost: float, cities: List[City]) -> None:
    file = open("output.txt", "w")
    file.write(f"{min_cost}\n")
    for city in cities:
        file.write(f"{city.x} {city.y} {city.z}\n")
    file.close()