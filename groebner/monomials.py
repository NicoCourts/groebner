from math import factorial
from warnings import warn
from random import randint


class MonomialOrdering():
    """Has information pertaining to the ordering of monomials as well as 
        conversions between lists of coefficients and polynomials"""
    def __init__(self, num_vars, labels=None, order_type='grlex'):
        self.num_vars = num_vars
        
        if labels is None:
            # if no variable labels are provided, we make our own
            self.var_labels = []
            for i in range(num_vars):
                self.var_labels.append(f'x_{i}')
        else:
            # if the user does something silly here it might not look great,
            #   but shouldn't break things.
            if type(labels) is not list:
                self.var_labels = [str(labels)]
            else:
                self.var_labels = list(map(str, labels))
        
        if order_type == 'grlex':
            self.lt = self._lt_grlex
        elif order_type == 'lex':
            self.lt = self._lt_lex
        elif order_type == 'grevlex':
            self.lt = self._lt_grevlex
        else:
            raise NotImplementedError('Only implemented for "lex", "grlex", and "grevlex" orderings.')
        
        # TODO Implement grevlex, which should be faster.

        # always assume variables have decreasing order
        # x_1 > x_2 > x_3 > ... > x_n
        # In total degree k, there are (n+k-1) C (n-1) monomials

    # we want to expose the "variables" (monomials of degree 1)
    def get_vars(self):
        vars = {}
        for i in range(self.num_vars):
            lst = [0]*(self.num_vars)
            lst[i] = 1
            vars[self.var_labels[i]] = Monomial(lst, self)
        return vars
    
    def constant_monomial(self):
        return Monomial([0]*(self.num_vars), self)
    
    def random(self, deg_bound=20):
        degs = []
        for _ in range(self.num_vars):
            degs.append(randint(0, deg_bound))
        return Monomial(degs, self)
    
    def _lt_grlex(self, a, b):
        # We only need less than. The rest can be defined from this.
        try:
            assert a.order == b.order
            # check degree
            if a.total_degree < b.total_degree:
                return True
            elif a.total_degree > b.total_degree:
                return False
            else:
                for i in range(len(a.degrees)):
                    if a.degrees[i] < b.degrees[i]:
                        return True
                    if a.degrees[i] > b.degrees[i]:
                        return False
                return False
        except AttributeError:
            raise ValueError("Can only compare items of type Monomial.")
        except (IndexError, AssertionError):
            raise ValueError("Monomials must be from same order.")
    
    def _lt_lex(self, a, b):
        try:
            assert a.order == b.order
            for i in range(len(a.degrees)):
                if a.degrees[i] < b.degrees[i]:
                    return True
                elif a.degrees[i] > b.degrees[i]:
                    return False
            return False
        except AttributeError:
            raise ValueError("Can only compare items of type Monomial.")
        except AssertionError:
            raise ValueError('Monomials must be from same order.')
    
    def _lt_grevlex(self, a, b):
        try:
            assert a.order == b.order
            if a.total_degree < b.total_degree:
                return True
            elif a.total_degree > b.total_degree:
                return False
            else:
                for i in range(len(a.degrees)):
                    idx = len(a.degrees) - 1 - i
                    if a.degrees[idx] < b.degrees[idx]:
                        # REVERSE the result
                        return False
                    elif a.degrees[idx] > b.degrees[idx]:
                        return True
                return False
        except AttributeError:
            raise ValueError("Can only compare items of type Monomial.")
        except AssertionError:
            raise ValueError('Monomials must be from same order.')
        
    def _get_total_degree(self, idx):
        # "spin off" graded pieces (total degree)
        if idx == 0:
            return 0, 0
        i = 1
        while idx > self._choose(self.num_vars + i - 1, self.num_vars - 1):
            idx -= self._choose(self.num_vars + i - 1, self.num_vars - 1)
            i += 1
        
        return i, idx

    def __contains__(self, other):
        if type(other) is not Monomial:
            return False
        else:
            return self.__eq__(other.order)
    
    def __eq__(self, other):
        if type(other) is not MonomialOrdering:
            return False
        
        return (self.num_vars == other.num_vars and
                self.var_labels == other.var_labels)
    
    def _choose(self, n, k):
        return factorial(n)/(factorial(k)*factorial(n-k))

class Monomial():
    """Wrapper for a list that represents a monomial"""
    def __init__(self, degrees, order):
        is_not_int = lambda x: type(x) is not int
        errors = sum(list(map(is_not_int, degrees)))
        if type(degrees) is not list or errors > 0:
            raise TypeError("Monomial only accepts a list of ints.")

        self.degrees = degrees
        self.total_degree = sum(degrees)
        self.order = order
        self.num_vars = self.order.num_vars

    def __mul__(self, other):
        # for now we only allow multiplication with other monomials
        if type(other) is not Monomial:
            raise TypeError('Monomials can only be multipled by other monomials.')
        if self.order != other.order:
            raise ValueError('Can only multiply monomials with compatible'
                             'monomial orderings.')

        degrees = [self.degrees[i] + other.degrees[i] for i in range(self.num_vars)]

        return Monomial(degrees, self.order)
    
    def __eq__(self, other):
        if type(other) is not Monomial:
            return False
        return self.degrees == other.degrees and self.order == other.order
    
    def __lt__(self, other):
        return self.order.lt(self, other)
    
    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)
    
    def __gt__(self, other):
        if type(other) is not Monomial:
            raise TypeError('Can only compare monomials with others.')
        return other.__lt__(self)
    
    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)
    
    def __repr__(self):
        s = ''
        var = self.order.get_vars()
        for i, lbl in enumerate(var.keys()):
            if self.degrees[i] > 0:
                s += lbl
                if self.degrees[i] > 1:
                    s += '^' + str(self.degrees[i])
        return s
    
    def __hash__(self):
        # let's just punt to tuples
        return tuple(self.degrees).__hash__()

    def _choose(self, n, k):
        return factorial(n)/(factorial(k)*factorial(n-k))