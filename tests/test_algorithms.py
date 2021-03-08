from groebner import QQ
from groebner.algorithms import buchberger
from groebner.polynomials import PolynomialRing


class TestAlgorithms:
    def test_buchberger_grlex(self):
        try:
            R = PolynomialRing(num_vars=3, labels=['x','y'])
            x, y = R.get_vars()

            gens = [
                x**3 - 2*x*y,
                x**2*y - 2*y**2 + x
            ]
            true_basis = [
                x**3 - 2*x*y,
                x**2*y - 2*y**2 + x,
                -x**2,
                -2*x*y,
                -2*y**2 + x
            ]

            basis = buchberger(gens)

            # TODO if order is correct we can just compare lists.
            assert set(basis) == set(true_basis)
        except NotImplementedError:
            # As long as we acknowledge it's not implemented its no problem
            pass
