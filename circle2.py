import math


class Circle:

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, r):
        if r < 0:
            raise ValueError("Radius should be nonnegative")
        self._r = r

    def __str__(self):
        return "Circle(x={}, y={}, r={})".format(self.x, self.y, self.r)

    def __add__(self, other):
        return Circle(self.x + other.x, self.y + other.y, self.r + other.r)

    def area(self):
        return math.pi * self._r ** 2
