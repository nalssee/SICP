""" A simple lisp parser for SICP exercises

Mostly from norvig.com,
just using a coroutine instead of lists.
"""

import re

__all__ = ["parse"]


def tokenize(expr):
    regex = re.compile("""(
    '|                        # quote
    \(|                       # left paren
    \)|                       # right paren
    [\w.?!+-></=*+]+|         # identifier
    ".*?"|                    # string
    )
    """, re.VERBOSE)
    return (x for x in re.findall(regex, expr) if x != '')


def parse(code):
    p = read_from_tokens()
    p.send(None)
    try:
        for token in tokenize(code):
            p.send(token)
    except StopIteration as e:
        return e.value

# coroutine
def read_from_tokens():
    """Constructs a list from tokens.
    """
    token = yield
    if token == '(':
        result = []
        while True:
            r0 = yield from read_from_tokens()
            if r0 == ')':
                break
            result.append(r0)
        return result
    # handle quotes
    elif token == "'":
        r0 = yield from read_from_tokens()
        return ['quote', r0]
    return atom(token)


def atom(x):
    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return x


if __name__ == "__main__":

    import unittest

    class LispParserTest(unittest.TestCase):
        def test_simple(self):
            code = """
            (define (gcd a b)
              (if (= b 0)
                  a
                  (gcd b (rem a b))))
            """
            self.assertEqual(parse(code),
                             ['define', ['gcd', 'a', 'b'],
                              ['if', ['=', 'b', 0],
                               'a',
                               ['gcd', 'b', ['rem', 'a', 'b']]]]
            )

        def test_simpler(self):
            self.assertEqual(parse('3'), 3)
            self.assertEqual(parse('-3.34'), -3.34)
            self.assertEqual(parse('"abc"'), '"abc"')
            self.assertEqual(parse("'a"), ['quote', 'a'])

        def test_string(self):
            code = """
            (define (fib n)
              "Computes nth fibonacci number"
              (if (< n 2)
                n
                (+ (fib (- n 1)) (fib (- n 2)))))
            """
            self.assertEqual(parse(code),
                             ['define', ['fib', 'n'],
                              '"Computes nth fibonacci number"',
                              ['if', ['<', 'n', 2],
                               'n',
                               ['+', ['fib', ['-', 'n', 1]],
                                ['fib', ['-', 'n', 2]]]]]
            )

        def test_quotes(self):
            code = """
            (define his-name  ''(kenjin che))
            """
            self.assertEqual(parse(code),
                             ['define', 'his-name', ['quote', ['quote', ['kenjin', 'che']]]]
            )




    unittest.main()
