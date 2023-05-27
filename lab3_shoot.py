from decimal import Decimal

import matplotlib.pyplot as plt
import numpy as np

from shoot_method.methods.rk import RK4
from shoot_method.methods.euler import Euler
from shoot_method.methods.euler2 import Euler2
from shoot_method.shoot import Shoot

from config import a, f, g, counts


def right1(y, dy):
    return y - Decimal('1').exp() - Decimal('1') / Decimal(
        '1').exp() + Decimal('2')


def dright1(r, dr):
    return r


def right2(y, dy):
    return dy - Decimal('1').exp() + Decimal(
        '1') / Decimal('1').exp() - Decimal(str(a))


def dright2(r, dr):
    return dr


def right3(y, dy):
    return dy + y - Decimal('2') * Decimal(
        '1').exp() - Decimal(str(a)) + Decimal('2')


def dright3(r, dr):
    return dr + r


right_shoot = {
    'б': (right1, dright1),
    'г': (right2, dright2),
    'е': (right3, dright3),
}

left_shoot = {
    # 'а': (lambda mu: Decimal('0'), None),
    'в': (lambda mu: -Decimal(str(a)), lambda mu: Decimal('0')),
    'д': (lambda mu: mu - Decimal(str(a)), lambda mu: Decimal('1'))
}

shoot_methods = {
    'Эйлер': (Euler(lambda x, y, dy: dy, f), Euler(lambda x, r, dr: dr, g)),
    'Эйлер с пересчетом': (
        Euler2(lambda x, y, dy: dy, f), Euler2(lambda x, r, dr: dr, g)),
    'Рунге-Кута': (RK4(lambda x, y, dy: dy, f), RK4(lambda x, r, dr: dr, g))
}


def shoot(left_name, right_name):
    print('метод стрельбы')
    print()

    print(f'левое краевое условие: {left_name}')
    dy_a, dr_a = left_shoot[left_name]
    print(f'правое краевое условие: {right_name}')
    phi_b, dphi_b = right_shoot[right_name]

    # fig, ax = plt.subplots(1, len(counts))
    # figs = []

    res = {
        'Эйлер': {},
        'Эйлер с пересчетом': {},
        'Рунге-Кута': {}
    }

    for count in counts:
        print(f'кол-во точек: {count}')

        # fig, ax = plt.subplots()
        # ax.set_title(f'n = {count}')
        # ax.set_xlabel("x")
        # ax.set_ylabel("y")
        # figs.append(fig)

        for name, met in shoot_methods.items():
            print(f'решаем методом {name}')

            sh = Shoot(met[0], met[1], count)

            y_s = sh.make1(dy_a, dr_a, phi_b, dphi_b, None)  # временно

            # ax.plot(np.linspace(0, 1, count), y_s, label=f'{name}')

            res[name][count] = y_s

            np.savetxt(
                f'results/{name}_{count}.csv',
                (np.linspace(0, 1, count), y_s),
                delimiter=','
            )
        # ax.legend()
    print()

    return res
    # plt.show()
