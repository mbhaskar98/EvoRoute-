class City:
    def __init__(self, x: int, y: int, z: int):
            self.x = x
            self.y = y
            self.z = z

    def __str__(self):
        return f"City({self.x}, {self.y}, {self.z})"
    
    def __repr__(self):
         return self.__str__()

    def distance(self, other: 'City') -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5