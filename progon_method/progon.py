from decimal import Decimal

import numpy as np

N = Decimal('20')  # ваш номер в списке
a = Decimal('2') + Decimal('0.1') * N


def _row_i(h):
    return Decimal('1'), - Decimal('2') - h * h, Decimal('1')


def _free_i(x_i, h):
    return h * h * (Decimal('2') * a + a * (1 - x_i) + Decimal('2'))


class Progon:
    def __init__(self, row_i, free_i, maker, count):
        self.free_i = free_i
        self.maker = maker
        self.row_i = row_i

        self.count = count
        self.h = Decimal('1.0') / Decimal(str(count))

        self.xs = np.linspace(0, 1, count + 1)

    def matrix1(self, row_0, row_n):
        mx = np.zeros((self.count + 1, self.count + 1), dtype=object)

        for i in (0, 1):
            mx[0, i] = row_0(self.h)[i]

        for i in range(1, self.count):
            for j in (-1, 0, 1):
                mx[i, i + j] = self.row_i(self.h)[j + 1]

        for i in (0, 1):
            mx[self.count, self.count - 1 + i] = row_n(self.h)[i]

        return mx

    def matrix2(self, row_0, row_n):
        mx = np.zeros((self.count + 1, self.count + 1), dtype=object)

        for i in (0, 1, 2):
            mx[0, i] = row_0(self.h)[i]

        for i in range(1, self.count):
            for j in (-1, 0, 1):
                mx[i, i + j] = self.row_i(self.h)[j]

        for i in (0, 1, 2):
            mx[self.count, self.count - 2 + i] = row_n(self.h)[i]

        for i in (0, 1, 2):
            mx[0, i] = mx[0, i] + mx[1, i]
            mx[
                self.count, self.count - 2 + i
            ] = mx[self.count, self.count - 2 + i] - \
                mx[self.count - 1, self.count - 2 + i]

        return mx

    def free_vector(self, free_0, free_n):
        mx = np.zeros(self.count + 1, dtype=object)

        mx[0] = free_0(self.h)

        for i in range(1, self.count):
            mx[i] = self.free_i(Decimal(str(self.xs[i])), self.h)

        mx[self.count] = free_n(self.h)

        return mx

    def make1(self, row_0, row_n, free_0, free_n):
        mx = self.matrix1(row_0, row_n)
        vec = self.free_vector(free_0, free_n)
        result = self.maker(mx, vec)

        return result

    def make2(self, row_0, row_n, free_0, free_n):
        mx = self.matrix2(row_0, row_n)
        vec = self.free_vector(free_0, free_n)
        result = self.maker(mx, vec)

        return result
