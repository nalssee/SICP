import os
import sys

TESTPATH = os.path.dirname(os.path.realpath(__file__))
PYPATH = os.path.join(TESTPATH, '..', '..')
sys.path.append(PYPATH)

from SICP.lisp_parser import parse
from SICP.lisp import *
import unittest


def ev(exp, env=Env()):
    return evaluate(parse(exp), env)


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


    def test_define_simple(self):
        env = Env()
        evaluate(parse('(define a 20)'), env)
        self.assertEqual(evaluate(parse('a'), env), 20)
        evaluate(parse("(define b 'abc)"), env)
        self.assertEqual(evaluate(parse('b'), env), 'abc')
        evaluate(parse("(define a '30.3)"), env)
        self.assertEqual(evaluate(parse('a'), env), 30.3)

    def test_assignment_simple(self):
        env = Env()
        evaluate(parse('(define a 10)'), env)
        self.assertEqual(evaluate(parse('a'), env), 10)
        evaluate(parse('(set! a 30)'), env)
        self.assertEqual(evaluate(parse('a'), env), 30)
        with self.assertRaises(UnboundVar):
            evaluate(parse('(set! b 10)'), env)

    def test_if(self):
        self.assertEqual(ev('(if true 10 20)'), 10)
        self.assertEqual(ev('(if 1 10 20)'), 10)
        self.assertEqual(ev('(if false 10 20)'), 20)

    def test_eval_sequence(self):
        self.assertEqual(ev('(begin 10 20 false)'), 'false')

    def test_lambda(self):
        proc = ev('(lambda (x y) (+ x y))')
        self.assertEqual(proc.params, ['x', 'y'])
        self.assertEqual(proc.body, ['+', 'x', 'y'])

unittest.main()
