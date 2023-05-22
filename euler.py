from decimal import Decimal

import diff_base


class Euler(diff_base.Diff):
    def __init__(self, f, g):
        super().__init__(f, g)

    def step(self, x, y, dy, h) -> (Decimal, Decimal):
        return (y + h * self.f(x, y, dy),
                dy + h * self.g(x, y, dy))

