import operator
from collections import namedtuple


class cons(namedtuple('cons', 'car, cdr')):
    __slots__ = ()
    def __str__(self):
        elts = [str(self.car)]
        cdr = self.cdr

        while isinstance(cdr, cons):
            elts.append(str(cdr.car))
            cdr = cdr.cdr
        if cdr != []:
            elts.append('.')
            elts.append(str(cdr))
        return '(' + ' '.join(elts) + ')'


def plus(*xs):
    return sum(xs)

def minus(*xs):
    first, *rest = xs
    for x in rest:
        first -= x
    return first

def mult(*xs):
    result = 1
    for x in xs:
        result *= x
    return result

def div(*xs):
    first, *rest = xs
    for x in rest:
        first /= x
    return first

def is_null(x):
    return 'true' if x == [] else 'false'

def car(pair):
    return pair.car

def cdr(pair):
    return pair.cdr

def lisp_list(*args):
    args = list(args)
    result = []
    while args:
        result = cons(args.pop(), result)
    return result

def lisp_not(x):
    return 'true' if not x else 'false'

def lisp_compare(xs, pred):
    for x1, x2 in zip(xs, xs[1:]):
        if not pred(x1, x2):
            return 'false'
    return 'true'

def lisp_eq(*xs):
    return lisp_compare(xs, operator.eq)

def lisp_lt(*xs):
    return lisp_compare(xs, operator.lt)

def lisp_gt(*xs):
    return lisp_compare(xs, operator.gt)

def lisp_le(*xs):
    return lisp_compare(xs, operator.le)

def lisp_ge(*xs):
    return lisp_compare(xs, operator.ge)
