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
    def _parse(expr):
        p = read_from_tokens()
        p.send(None)
        try:
            for token in tokenize(expr):
                p.send(token)
        except StopIteration as e:
            return e.value

    def handle_quote(parsed):
        if isinstance(parsed, list):
            if parsed == []:
                return []
            a, *b = parsed
            if a == "'":
                return [["quote"] + handle_quote(b)]
            return [handle_quote(a)] + handle_quote(b)
        return parsed

    return handle_quote(_parse(code))


def read_from_tokens():
    """Constructs a list from tokens.
    """
    token = yield
    if token == '(':
        result = []
        while True:
            r0 = yield from read_from_tokens()
            if r0 == ')': break
            result.append(r0)
        return result
    elif token == ')':
        return token
    else:
        return atom(token)


def atom(x):
    """Identifies what x means as a lisp token.

    If x is enclosed with quotation marks, a tuple ("string", x)
    elif x can be coerced to a number, it is returned as so.
    """
    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            if x[0] == '"' and x[-1] == '"':
                return ("string", x[1:-1])
            else:
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
                              ('string', "Computes nth fibonacci number"),
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
