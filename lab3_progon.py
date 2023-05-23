import matplotlib.pyplot as plt
import numpy as np

from progon_method.progon import Progon
from progon_maker import tridiagonal_solve
from config import a, p, q, counts

left_progon = {
    'O(h^1)': {
        'а': (lambda h: (1, 0), lambda h: 0),
        'в': (lambda h: (-1, 1), lambda h: -a * h),
        'д': (lambda h: (- 1 - h, 1), lambda h: -a * h)
    },
    'O(h^2)': {
        'а': (lambda h: (1, 0), lambda h: 0),
        'в': (
            lambda h: (-2, 2 - h * h),
            lambda h: - 2 * h * a + h * h * q(h)
        ),
        'д': (
            lambda h: (- 2 - 2 * h, 2 - h * h),
            lambda h: - 2 * h * a + h * h * q(h)
        )
    }
}

right_progon = {
    'O(h^1)': {
        'б': (
            lambda h: (0, 1),
            lambda h: np.e + 1 / np.e - 2
        ),
        'г': (
            lambda h: (1, -1),
            lambda h: - h * (np.e - 1 / np.e + a)
        ),
        'е': (
            lambda h: (1, - 1 + h),
            lambda h: - h * (2 * np.e + a - 2)
        )
    },
    'O(h^2)': {
        'б': (
            lambda h: (0, 1),
            lambda h: np.e + 1 / np.e - 2
        ),
        'г': (
            lambda h: (- 2 + h * h, 2),
            lambda h: 2 * h * (np.e - 1 / np.e + a) - h * h * q(1 - h)
        ),
        'е': (
            lambda h: (- 2 + h * h, 2 + 2 * h),
            lambda h: 2 * h * (2 * np.e + a - 2) - h * h * q(1 - h)
        )
    }
}

# left_progon_Oh1 = {
#     'а': (lambda h: (1, 0), lambda h: 0),
#     'в': (lambda h: (-1, 1), lambda h: -a * h),
#     'д': (lambda h: (- 1 - h, 1), lambda h: -a * h)
# }

# right_progon_Oh1 = {
#     'б': (
#         lambda h: (0, 1),
#         lambda h: np.e + 1 / np.e - 2
#     ),
#     'г': (
#         lambda h: (1, -1),
#         lambda h: - h * (np.e - 1 / np.e + a)
#     ),
#     'е': (
#         lambda h: (1, - 1 + h),
#         lambda h: - h * (2 * np.e + a - 2)
#     )
# }
#
# left_progon_Oh2 = {
#     'а': (lambda h: (1, 0), lambda h: 0),
#     'в': (
#         lambda h: (-2, 2 - h * h),
#         lambda h: - 2 * h * a + h * h * q(h)
#     ),
#     'д': (
#         lambda h: (- 2 - 2 * h, 2 - h * h),
#         lambda h: - 2 * h * a + h * h * q(h)
#     )
# }
#
# right_progon_Oh2 = {
#     'б': (
#         lambda h: (0, 1),
#         lambda h: np.e + 1 / np.e - 2
#     ),
#     'г': (
#         lambda h: (- 2 + h * h, 2),
#         lambda h: 2 * h * (np.e - 1 / np.e + a) - h * h * q(1 - h)
#     ),
#     'е': (
#         lambda h: (- 2 + h * h, 2 + 2 * h),
#         lambda h: 2 * h * (2 * np.e + a - 2) - h * h * q(1 - h)
#     )
# }


def progon(left_name, right_name):
    print('метод разностной прогонки')

    res = {
        'O(h^1)': {},
        'O(h^2)': {}
    }

    for acc in ('O(h^1)', 'O(h^2)'):
        left = left_progon[acc][left_name]
        right = right_progon[acc][right_name]

        for count in counts:
            pr = Progon(p, q, tridiagonal_solve, count)
            y_s = pr.make(left, right)
            res[acc][count] = y_s

            np.savetxt(
                f'results/progon_{acc}_{count}.csv',
                (np.linspace(0, 1, count + 1), y_s),
                delimiter=','
            )

    return res


def test():
    res = progon('д', 'г')

    plt.plot(np.linspace(0, 1, 101), res['O(h^1)'][100], color='c')
    plt.plot(np.linspace(0, 1, 101), res['O(h^2)'][100], color='k')

    xs = np.linspace(0, 1, 150)
    ys = -2 - 4 * xs + 4 * xs * xs + np.exp(xs) + np.exp(-xs)

    plt.plot(xs, ys, color='r', label='Аналитическое решение')

    plt.show()

if __name__ == '__main__':
    test()