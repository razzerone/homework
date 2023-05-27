from decimal import Decimal

import numpy as np
from matplotlib import pyplot as plt

from lab3_shoot import shoot, shoot_methods
from lab3_progon import progon

from config import left, right, counts, colors, a

# не забудь поменять условие в файле config

if __name__ == '__main__':
    # условие 'а' пока не работает
    res_shoot = shoot(left, right)
    res_progon = progon(left, right)

    figs = []

    for count in counts:
        fig, ax = plt.subplots()
        ax.set_title(f'n = {count}')
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        figs.append(fig)

        color_count = 0

        xs = np.linspace(0, 1, 150)
        ys = -2 - a * xs + a * xs * xs + np.exp(xs) + np.exp(-xs)

        ax.plot(xs, ys, color='r', label='Аналитическое решение')

        for name, met in shoot_methods.items():
            ax.plot(
                np.linspace(0, 1, count),
                res_shoot[name][count],
                label=f'{name}',
                color=colors[color_count]
            )
            color_count += 1

        for acc in ('O(h^1)', 'O(h^2)'):
            ax.plot(
                np.linspace(0, 1, count + 1),
                res_progon[acc][count],
                label=f'Разностная прогонка {acc}',
                color=colors[color_count]
            )
            color_count += 1

        ax.legend()

    plt.show()
