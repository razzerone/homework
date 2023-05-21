from _decimal import Decimal
from typing import Tuple


def tridiagonal_solve(
        main_matrix,
        free_members):
    """
    :param main_matrix: main matrix, must be square (n x n) and tridiagonal,
        outer tuple is a tuple of rows, i.e. ((0, 1, 2), (1, 0, 4), (0, 2, 1) represents matrix
        0 1 2
        1 0 4
        0 2 1
    :param free_members: free members column values, dimension must align with main matrix
    :return: a solution of AX=B matrix equation, where X is unknown, A is main matrix, B is free members column
    """

    n = len(main_matrix)

    def a(j: int) -> Decimal:
        if j <= 0:
            raise ValueError()
        return main_matrix[j, j - 1]

    def b(j: int) -> Decimal:
        return main_matrix[j, j]

    def c(j: int) -> Decimal:
        if j >= n - 1:
            raise ValueError()
        return main_matrix[j, j + 1]

    alpha = list(None for _ in range(n))
    beta = list(None for _ in range(n))

    y = b(0)
    alpha[0] = -c(0) / y
    beta[0] = free_members[0] / y

    for i in range(1, n):
        y = b(i) + a(i) * alpha[i - 1]

        if i < n - 1:
            alpha[i] = -c(i) / y

        beta[i] = (free_members[i] - a(i) * beta[i - 1]) / y

    result = list(None for _ in range(n))

    result[n - 1] = beta[n - 1]
    for i in reversed(range(n - 1)):
        result[i] = alpha[i] * result[i + 1] + beta[i]

    return tuple(result)
