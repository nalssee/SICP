# for 03
import heapq
import time
from random import randint
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


# 22
def time_tag(func):
    "Prints the time it took"
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print("It took %f seconds" % (end - start))
    return wrapper


def is_prime(n):
    return smallest_divisor(n) == n


def search_for_prime(a, test_fn):
    """search for prime numbers from a
    """
    while True:
        if test_fn(a):
            yield a
        a += 1


def ex22():
    @time_tag
    def three_primes(n):
        """three smallest prime numbers from n
        """
        for i in islice(search_for_prime(n, is_prime), 3):
            print(i)
    # see for yourself
    three_primes(100000)
    three_primes(10000000)
    three_primes(1000000000)

# ex22()


# 23
def smallest_divisor1(n):
    def find_devisor(n, test_val):
        while test_val ** 2 < n:
            if n % test_val == 0:
                return test_val
            else:
                if test_val == 2:
                    test_val = 3
                else:
                    test_val += 2
        return n
    return find_devisor(n, 2)


def is_prime1(n):
    return smallest_divisor1(n) == n


def ex23():
    @time_tag
    def three_primes(n):
        """three smallest prime numbers from n
        """
        for i in islice(search_for_prime(n, is_prime1), 3):
            print(i)
    # see for yourself
    three_primes(100000)
    three_primes(10000000)
    three_primes(1000000000)

# ex23()


# 24

def expmod(base, exp, m):
    if exp == 0:
        return 1
    elif exp % 2 == 0:
        return (expmod(base, exp // 2, m) ** 2) % m
    else:
        return (base * expmod(base, exp - 1, m)) % m

# def expmod(base, exp, m):
#     return fast_expt(base, exp) % m


def fermat_test(n):
    a = randint(1, n - 1)
    return expmod(a, n, n) == a


def is_prime_fast(n, times=5):
    if times == 0:
        return True
    elif fermat_test(n):
        return is_prime_fast(n, times - 1)
    else:
        return False


def ex24():
    @time_tag
    def three_primes(n):
        """three smallest prime numbers from n
        """
        for i in islice(search_for_prime(n, is_prime_fast), 3):
            print(i)
    # see for yourself
    three_primes(100000)
    three_primes(10000000)
    three_primes(1000000000)

# ex24()


# 25
# It doesn't work because you have to compute exponential first with Alyssa's idea
# it costs a lot


# 26
# It's really stupid
# See ex 2.43

# 27
def carmichael_test(n):
    return all(expmod(i, n, n) == i for i in range(2, n))

carmichael_numbers = [561, 1105, 1729, 2465, 2821, 6601]
def ex27():
    print()
    for n in carmichael_numbers:
        print("Carmichael: ", carmichael_test(n), "|  Prime: ", is_prime(n))

# ex27()


# 28
# boring, skipping


# 29
def integral(f, a, b, n):
    h = (b - a) / n

    total = 0
    for k in range(1, n, 2):
        y0 = f(a + (k - 1) * h)
        y1 = f(a + k * h)
        y2 = f(a + (k + 1) * h)
        total += y0 + 4 * y1 + y2
    return total * h / 3

# pretty accurate
# print(integral(lambda x: x ** 3, 0, 1, 100))


# 30
# Python doesn't generally support TCO
# So, you can't just follow as shown in the exercise
# but, do you see any difference?
def sum(term, a, next, b):
    result = 0
    while a <= b:
        result += term(a)
        a = next(a)
    return result
