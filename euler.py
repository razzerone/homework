from decimal import Decimal

import diff_base


class Euler(diff_base.Diff):
    def __init__(self, f, g):
        super().__init__(f, g)

    def step(self, x_, y_, dy_, h) -> (Decimal, Decimal):
        return (x_ + h * self.f(x_, y_),
                y_ + h * self.g(x_, y_))

