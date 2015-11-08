import os
import sys

TESTPATH = os.path.dirname(os.path.realpath(__file__))
PYPATH = os.path.join(TESTPATH, '..', '..', '..')
sys.path.append(PYPATH)

from SICP.vseval.parser import parse
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
