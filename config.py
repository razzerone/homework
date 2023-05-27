from decimal import Decimal

########
N = 20  # ваш номер в списке
a = 2 + 0.1 * N
########
# не советую брать 'а' и 'е'
left = 'в'
right = 'г'
########

# для стрельбы


def f(x, y, dy):
    return y + Decimal('2') * Decimal(str(a)) + Decimal(
        '2') + Decimal(str(a)) * x * (Decimal('1') - x)


def g(x, r, dr):
    # r'' = g()
    # g() = df_y * r + df_dy * r'
    return r


# для прогонки
def p(x):
    return 1


def q(x):
    return 2.0 + 2.0 * a + a * x * (1 - x)


counts = [
    10,
    20,
    50,
    100
]

colors = [
    'b', 'orange', 'g', 'c', 'm'
]
