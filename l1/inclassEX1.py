class Vector:
    def __init__(self, x, y):
        self.x, self.y = x,y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

v1, v2 = Vector(1,2), Vector(3,4)
print(v1 + v2, v1 - v2, v1 == v2, v1 * 3)
