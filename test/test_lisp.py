import os
import sys

TESTPATH = os.path.dirname(os.path.realpath(__file__))
PYPATH = os.path.join(TESTPATH, '..', '..')
sys.path.append(PYPATH)

from SICP.lisp_parser import parse
from SICP.lisp import *
import unittest


class EVALTest(unittest.TestCase):
    def test_selfeval(self):
        self.assertEqual(evaluate(parse('30'), Env()), 30)
        self.assertEqual(evaluate(parse("32.3"), Env()), 32.3)
        self.assertEqual(evaluate(parse('  "Hello World!"  '), Env()), '"Hello World!"')

    def test_lookup_simple(self):
        env = Env({'a': 30})

        self.assertEqual(evaluate(parse('a'), env), 30)
        with self.assertRaises(UnboundVar):
            evaluate(parse('b'), env)

        env.upper = Env({'b': 20})
        self.assertEqual(evaluate(parse('b'), env), 20)

    def test_quote(self):
        self.assertEqual(evaluate(parse("'abc"), Env()), 'abc')
        self.assertEqual(evaluate(parse("' (a b c )"), Env()), ['a', 'b', 'c'])


    def test_assign(self):
        env = Env()
        evaluate(parse('(set! a 20)'), env)
        self.assertEqual(evaluate(parse('a'), env), 20)
        evaluate(parse("(set! b 'abc)"), env)
        self.assertEqual(evaluate(parse('b'), env), 'abc')
        evaluate(parse("(set! a '30.3)"), env)
        self.assertEqual(evaluate(parse('a'), env), 30.3)

    # Wondering if I should distinguish set! and define

unittest.main()
