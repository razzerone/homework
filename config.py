from decimal import Decimal

N = Decimal('20')  # ваш номер в списке
a = Decimal('2') + Decimal('0.1') * N

def f(x, y, dy):
    return y + Decimal('2') * a + Decimal('2') + a * x * (Decimal('1') - x)


def g(x, r, dr):
    # r'' = g()
    # g() = df_y * r + df_dy * r'
    return r