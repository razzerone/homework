from decimal import Decimal

from diff_base import Diff


class Shoot:
    def __init__(
            self,
            diff_method_y: Diff,
            diff_method_r: Diff,
            count
    ):
        self.count = count
        self.diff_method_y = diff_method_y
        self.diff_method_r = diff_method_r

    def make1(self, dy_a, dr_a, phi_b, dphi_b, stop):
        # phi(y(b), dy(b))
        mu = Decimal("1.0000000001")

        while 1:
            y_s, dy_s = self.diff_method_y.make(mu, dy_a(mu), self.count)

            phi = phi_b(y_s[-1], dy_s[-1])

            # print('мю:', mu)
            # print('фи:', phi)
            # print(dy_s[0])

            r_s, dr_s = self.diff_method_r.make(1, dr_a(mu), self.count)

            dphi = dphi_b(r_s[-1], dr_s[-1])

            new_mu = mu - phi / dphi

            if abs(phi) < Decimal('0.000001'):
                return y_s

            mu = new_mu
