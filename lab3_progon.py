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
