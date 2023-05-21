from decimal import Decimal

from diff_base import Diff


class Euler2(Diff):
    def __init__(self, f, g):
        super().__init__(f, g)

    def step(self, x_, y_, dy_, h) -> (Decimal, Decimal):
        return (
            x_ + h / Decimal('2') * (
                        self.f(x_, y_) + self.f(x_ + h * self.f(x_, y_),
                                                y_ + h * self.g(x_, y_))),
            y_ + h / Decimal('2') * (
                        self.g(x_, y_) + self.g(x_ + h * self.f(x_, y_),
                                                y_ + h * self.g(x_, y_)))
        )
