# for 03
import heapq
import time
from functools import wraps
from itertools import islice

# 03
def sum_of_squares_of_the_largest_n(xs, n):
    return sum(x ** 2 for x in heapq.nlargest(n, xs))


# 07
# This version stacks up for each function call,
# because Python does not optimize tail calls.
def sqrt_iter1(guess, x):
    if is_good_enough(guess):
        return guess
    else:
        return sqrt_iter(improve(guess, x), x)


def sqrt_iter(guess, x):
    while True:
        test, guess = is_good_enough(guess, x)
        if test: break
    return guess


def is_good_enough(guess, x):
    improved_guess = improve(guess, x)
    return abs((guess - improved_guess) / guess) < 0.001, improved_guess


def improve(guess, x):
    return average(guess, x / guess)


def average(x, y):
    return (x + y) / 2


def sqrt(x):
    if x > 0:
        return sqrt_iter(1.0, x)
    else:
        raise ZeroDivisionError()


# 08
def cubic_root(x):
    return cubic_root_iter(1.0, x)


def cubic_root_iter(guess, x):
    while True:
        test, guess = is_good_enough_cubic(guess, x)
        if test: break
    return guess


def is_good_enough_cubic(guess, x):
    improved_guess = improve_cubic(guess, x)
    return abs((guess - improved_guess) / guess) < 0.001, improved_guess


def improve_cubic(guess, x):
    return (x / guess ** 2 + 2 * guess) / 3


# 10
# recursive version
def ackermann_rec(x, y):
    if y == 0: return 0
    elif x == 0: return 2 * y
    elif y == 1: return 2
    else: return ackermann_rec(x - 1, ackermann_rec(x, y - 1))


# non-recursive version using a stack
# although there's no computational advantage
# this one at least doesn't overflow a system stack
# try ackermann_rec(2, 5) and ackermann(2, 5)
def ackermann(x, y):
    # user defined stack
    s = []
    cont = "ack-done"
    label = "ack-loop"
    while True:
        if label == "ack-loop":
            if y == 0:
                val = 0
                label = cont
            elif x == 0:
                val = 2 * y
                label = cont
            elif y == 1:
                val = 2
                label = cont
            else:
                s.append(x)
                # s.append(y)
                s.append(cont)
                y = y - 1
                cont = "after-inner-call"
                label = "ack-loop"
        elif label == "after-inner-call":
            cont = s.pop()
            # y = s.pop()
            x = s.pop()
            x = x - 1
            y = val
            label = "ack-loop"
        else: break
    return val


# (h n) => 2 ^ (h (- n 1))
# (h 5) => 2^2^2^2^2 = 2 ^ 65536 which is an impossibly large number

def fib(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a

def fib_test(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
        pi = (1 + 5 ** 0.5) / 2
        approx = (pi ** (i + 1)) / 5 ** 0.5
        print("%5d  %10.2f  %f" % (a, approx, abs(a - approx) / a))


# 11
def f_rec(n):
    if n < 3: return n
    else: return f_rec(n - 1) + 2 * f_rec(n - 2) + 3 * f_rec(n - 3)


def f(n):
    a, b, c = 0, 1, 2
    for i in range(n):
        a, b, c = b, c, c + 2 * b + 3 * a
    return a


# 12
def pascal(n):
    if n == 1:
        return [1]
    else:
        prev = pascal(n - 1)
        inner = []
        for a, b in zip(prev, prev[1:]):
            inner.append(a + b)
        return [1] + inner + [1]


# 16
def fast_expt(b, n):
    if n == 1:
        return b
    elif n % 2 == 0:
        return fast_expt(b, n // 2) ** 2
    else:
        return b * fast_expt(b, n - 1)


def expt(b, n):
    result = 1
    while n > 0:
        if n % 2 == 0:
            n = n // 2
            b = b * b
        else:
            result = result * b
            n = n - 1
    return result


# 17 trivial

# 18
def mult(a, b):
    def mult_pos(a, b):
        """when a > 0
        """
        temp = 0
        while a > 1:
            if a % 2 == 0:
                a, b = a // 2, b + b
            else:
                a, b, temp = a - 1, b, b + temp
        return b + temp
    if a == 0 or b == 0:
        return 0
    if a < 0:
        return -mult_pos(-a, b)
    return mult_pos(a, b)

# 19
def dot22(X, Y):
    """matrix multiplication, 2 by 2
    """
    a, b, c, d = X
    e, f, g, h = Y
    return a * e + b * g, a * f + b * h \
        ,c * e + d * g, c * f + d * h

# Some computations are not neceassry,
# but this is clearer since we are accustomed to matrix notation.
def fast_fib(n):
    A = (1, 1, 1, 0)
    R = (1, 1, 1, 0)
    while n > 1:
        if n % 2 == 0:
            n = n // 2
            A = dot22(A, A)
        else:
            n -= 1
            R = dot22(R, A)
    return dot22(R, A)[3]


# 21
def find_divisor(n, test_divisor):
    while test_divisor ** 2 <= n:
        if n % test_divisor == 0:
            return test_divisor
        else:
            test_divisor += 1
    return n


def smallest_divisor(n):
    return find_divisor(n, 2)


def time_tag(func):
    """returns (exetime, func(*args, **kwargs))
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end= time.time()
        return (end - start, result)
    return wrapper


@time_tag
def is_prime(n):
    return smallest_divisor(n) == n


def search_for_prime(a):
    """search for prime numbers from n
    """
    for i in range(a, 10**100):
        t, test = is_prime(i)
        if test:
            yield t, i

def ex22():
    def three_primes(n):
        """three smallest prime numbers from n
        """
        for t, v in islice(search_for_prime(n), 3):
            print(" *** %d %6.10f " % (v, t))
    # see for yourself
    print()
    three_primes(100000)
    print()
    three_primes(10000000)
    print()
    three_primes(1000000000)
