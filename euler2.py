from decimal import Decimal

from diff_base import Diff


class Euler2(Diff):
    def __init__(self, f, g):
        super().__init__(f, g)

    def step(self, x, y, dy, h) -> (Decimal, Decimal):
        return (
            y + h / Decimal('2') * (
                        self.f(x, y, dy) + self.f(x, y + h * self.f(x, y, dy),
                                                dy + h * self.g(x, y, dy))),
            dy + h / Decimal('2') * (
                        self.g(x, y, dy) + self.g(x, y + h * self.f(x, y, dy),
                                                dy + h * self.g(x, y, dy)))
        )
