from groebner import QQ
from groebner.algorithms import buchberger, division_algorithm
from groebner.polynomials import PolynomialRing
from groebner.rationals import Rational


class TestAlgorithms:
    def test_buchberger_grlex(self):
        R = PolynomialRing(labels=['x','y'], order='grlex')
        x, y = R.get_vars()

        gens = [
            x**3 - 2*x*y,
            x**2*y - 2*y**2 + x
        ]
        true_basis = [
            x**3 - 2*x*y,
            x**2*y - 2*y**2 + x,
            x**2,
            x*y,
            y**2 - Rational(1, 2)*x
        ]

        basis = buchberger(gens)

        # TODO if order is correct we can just compare lists.
        assert basis == true_basis
    
    def test_division_by_self_grlex(self):
        R = PolynomialRing(labels=['x','y'])
        f = R.random(max_deg=20)

        [q], r = division_algorithm(f, [f])

        assert q == R.one() and r == R.zero()
    
    def test_not_divisible_grlex(self):
        R = PolynomialRing(labels=['x','y'])
        x, y = R.get_vars()

        f = x**2*y - x
        g = y**2 + y

        [q], r = division_algorithm(f, [g])

        assert q == R.zero() and r == f
    
    def test_example_one_grlex(self):
        R = PolynomialRing(labels=['x','y'])
        x, y = R.get_vars()

        f = x**2*y+x*y**2+y**2
        g = x*y-1
        h = y**2-1

        [d1, d2], r = division_algorithm(f, [g, h])

        assert d1 == x+y 
        assert d2 == R.one() 
        assert r == x+y+1
    
    def test_example_two_grlex(self):
        R = PolynomialRing(labels=['x','y'])
        x, y = R.get_vars()

        f = x**2*y+x*y**2+y**2
        g = x*y-1
        h = y**2-1

        [d1, d2], r = division_algorithm(f, [h, g])

        assert d1 == x+1
        assert d2 == x
        assert r == 2*x+1
    
    def test_random_division(self):
        R = PolynomialRing(labels=['x','y','z'])

        f = R.random(num_terms=10, max_deg=12, denominator_bound=10)
        g = R.random(num_terms=10, max_deg=10, denominator_bound=10)
        h = R.random(num_terms=10, max_deg=10, denominator_bound=10)
        k = R.random(num_terms=10, max_deg=10, denominator_bound=10)

        [d1, d2, d3], r = division_algorithm(f, [g, h, k])

        assert f == g*d1 + h*d2 + k*d3 + r