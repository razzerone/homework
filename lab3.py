from decimal import Decimal

import matplotlib.pyplot as plt

from rk import RK4
from shoot import Shoot
from progon import Progon
from progon_maker import tridiagonal_solve

import numpy as np

N = Decimal('20')  # ваш номер в списке
a = Decimal('2') + Decimal('0.1') * N


def f(x, y, dy):
    return y + Decimal('2') * a + Decimal('2') + a * x * (Decimal('1') - x)


def g(x, r, dr):
    # r'' = g()
    # g() = df_y * r + df_dy * r'
    return r


def right1(y, dy):
    return y - Decimal('1').exp() - Decimal('1') / Decimal(
        '1').exp() + Decimal('2')


def dright1(r, dr):
    return r


def right2(y, dy):
    return dy - Decimal('1').exp() + Decimal('1') / Decimal('1').exp() - a


def dright2(r, dr):
    return dr


def right3(y, dy):
    return dy + y - Decimal('2') * Decimal('1').exp() - a + Decimal('2')


def dright3(r, dr):
    return dr + r


counts = [
    # 10,
    # 20,
    # 50,
    100
]

right_shoot = {
    'б': (right1, dright1),
    'г': (right2, dright2),
    'е': (right3, dright3),
}

left_shoot = {
    # 'а': (lambda mu: Decimal('0'), None),
    'в': (lambda mu: -a, lambda mu: Decimal('0')),
    'д': (lambda mu: mu - a, lambda mu: Decimal('1'))
}

methods = {
    # 'euler': (Euler(lambda y, dy: dy, f), Euler(lambda r, dr: dr, g)),
    # 'euler2': (Euler2(lambda y, dy: dy, f), Euler2(lambda r, dr: dr, g)),
    'rk': (RK4(lambda x, y, dy: dy, f), RK4(lambda x, r, dr: dr, g))
}


def shoot(left_name, right_name):
    print('метод стрельбы')
    print()

    print(f'левое краевое условие: {left_name}')
    dy_a, dr_a = left_shoot[left_name]
    print(f'правое краевое условие: {right_name}')
    phi_b, dphi_b = right_shoot[right_name]

    for name, met in methods.items():
        print(f'решаем методом {name}')
        for count in counts:
            print(f'кол-во точек: {count}')
            sh = Shoot(met[0], met[1], count)

            y_s = sh.make1(dy_a, dr_a, phi_b, dphi_b, None)  # временно

            plt.plot(np.linspace(0, 1, count), y_s)

            np.savetxt(
                f'results/{name}_{count}.csv',
                (np.linspace(0, 1, count), y_s),
                delimiter=','
            )
    print()


def row_i(h):
    return Decimal('1'), - Decimal('2') - h * h, Decimal('1')

def free_i(x_i, h):
    return h * h * (Decimal('2') * a + a * (1 - x_i) + Decimal('2'))


left_progon_Oh1 = {
    'а': (lambda h: (Decimal('1'), Decimal('0')), lambda h: Decimal('0')),
    'в': (lambda h: (Decimal('-1'), Decimal('1')), lambda h: -a * h),
    'д': (lambda h: (Decimal('-1') - h, Decimal('1')), lambda h: -a * h)
}

right_progon_Oh1 = {
    'б': (
        lambda h: (Decimal('0'), Decimal('1')),
        lambda h: Decimal('1').exp() + Decimal('1') / Decimal(
            '1').exp() - Decimal('2')
    ),
    'г': (
        lambda h: (Decimal('-1'), Decimal('1')),
        lambda h: h * (
                Decimal('1').exp() - Decimal('1') / Decimal('1').exp() + a)
    ),
    'е': (
        lambda h: (Decimal('-1'), Decimal('1') + h),
        lambda h: h * (Decimal('2') * Decimal('1').exp() + a - Decimal('2'))
    )
}

left_progon_Oh2 = {
    'а': (
        lambda h: (Decimal('1'), Decimal('0'), Decimal('0')),
        lambda h: Decimal('0')
    ),
    'в': (
        lambda h: (Decimal('-3'), Decimal('4'), Decimal('-1')),
        lambda h: Decimal('-2') * a * h
    ),
    'д': (
        lambda h: (Decimal('-3') - 2 * h, Decimal('4'), Decimal('-1')),
        lambda h: Decimal('-2') * a * h
    )
}

right_progon_Oh2 = {
    'б': (
        lambda h: (Decimal('0'), Decimal('0'), Decimal('1')),
        lambda h: Decimal('1').exp() + Decimal('1') / Decimal(
            '1').exp() - Decimal('2')
    ),
    'г': (
        lambda h: (Decimal('1'), Decimal('-4'), Decimal('3')),
        lambda h: Decimal('2') * h * (
                Decimal('1').exp() - Decimal('1') / Decimal('1').exp() + a)
    ),
    'е': (
        lambda h: (
            Decimal('1'), Decimal('-4'), Decimal('3') + Decimal('2') * h
        ),
        lambda h: (Decimal('2') * h * (
                Decimal('2') * Decimal('1').exp() + a - Decimal('2'))
                   )
    )
}


def progon_Oh1(left_name, right_name):
    print('порядок точности: 1')
    left_m, left_free = left_progon_Oh1[left_name]
    right_m, right_free = right_progon_Oh1[right_name]

    for count in counts:
        progon = Progon(row_i, free_i, tridiagonal_solve, count)

        y_s = progon.make1(left_m, right_m, left_free, right_free)

        np.savetxt(
            f'results/progon_O(h^1)_{count}.csv',
            (np.linspace(0, 1, count + 1), y_s),
            delimiter=','
        )


def progon_Oh2(left_name, right_name):
    print('порядок точности: 2')
    left_m, left_free = left_progon_Oh2[left_name]
    right_m, right_free = right_progon_Oh2[right_name]

    for count in counts:
        progon = Progon(row_i, free_i, tridiagonal_solve, count)

        y_s = progon.make2(left_m, right_m, left_free, right_free)

        np.savetxt(
            f'results/progon_O(h^2)_{count}.csv',
            (np.linspace(0, 1, count + 1), y_s),
            delimiter=','
        )


def progon(left_name, right_name):
    print('метод разностной прогонки')
    print()
    progon_Oh1(left_name, right_name)
    progon_Oh2(left_name, right_name)
    print()


def main():
    #shoot('д', 'е')
    # в и г вместе не брать

    progon_Oh1('д', 'е')


if __name__ == '__main__':
    main()
