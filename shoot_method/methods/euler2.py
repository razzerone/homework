from decimal import Decimal

import numpy as np


class Euler2:
    def __init__(self, f, g):
        self.f = f
        self.g = g

    def make(self, y0, dy0, count: int):
        h = Decimal('1.0') / Decimal(str(count))

        res1 = [0] * count
        res2 = [0] * count

        lp = np.linspace(0, 1, count)

        res1[0] = y0
        res2[0] = dy0

        for i in range(count - 1):
            y, dy = self.step(Decimal(str(lp[i + 1])), y0, dy0, h)

            res1[i + 1] = y
            res2[i + 1] = dy

            y0, dy0 = y, dy

        return res1, res2

    def step(self, x, y, dy, h) -> (Decimal, Decimal):
        return (
            y + h / Decimal('2') * (
                        self.f(x, y, dy) + self.f(x, y + h * self.f(x, y, dy),
                                                dy + h * self.g(x, y, dy))),
            dy + h / Decimal('2') * (
                        self.g(x, y, dy) + self.g(x, y + h * self.f(x, y, dy),
                                                dy + h * self.g(x, y, dy)))
        )
