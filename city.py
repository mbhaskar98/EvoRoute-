class City:
    """
    A basic city class
    """

    def __init__(self, x: int, y: int, z: int):
            self.x = x
            self.y = y
            self.z = z

    def __str__(self):
        """
        Return a string representation of the city.
        """
        return f"City({self.x}, {self.y}, {self.z})"
    
    def __repr__(self):
         """
         Return a string representation of the city for debugging.
         """
         return self.__str__()

    def distance(self, other: 'City') -> float:
        """
        Given another city, return the Euclidean distance between the two cities.
        """
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5