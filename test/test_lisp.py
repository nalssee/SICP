import os
import sys

TESTPATH = os.path.dirname(os.path.realpath(__file__))
PYPATH = os.path.join(TESTPATH, '..', '..')
sys.path.append(PYPATH)

from SICP.lisp_parser import parse
from SICP.lisp import *
import unittest


def ev(exp, env=GLOBAL_ENV):
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
        self.assertEqual(ev("'(a (b) c )"), ev("(list 'a (list 'b) 'c)"))


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
        self.assertEqual(proc.body, [['+', 'x', 'y']])


    def test_builtins(self):
        self.assertEqual(ev('(+ 10 20 30)'), 60)
        self.assertEqual(ev('(- 10 20 30)'), -40)
        self.assertEqual(ev('(* 10 20 30)'), 6000)
        self.assertEqual(ev('(/ 10 20 30)'), 10 / 20 / 30)
        self.assertEqual(ev('(+ 1 (- 20 3) (* 4 5))'), 38)
        self.assertEqual(ev("(cons 1 (cons 2 (cons 3 '())))"),
                         ev("(list 1 2 3)"))
        env = GLOBAL_ENV
        ev('(define x (cons 1 (cons 2 3)))', env)
        self.assertEqual(ev('(car (cdr x))', env), 2)
        self.assertEqual(ev('(cdr (cdr x))', env), 3)

        self.assertEqual(ev("(if (not (null? '())) true false)", env), 'false')
        self.assertEqual(ev("(if (null? '()) true false)", env), 'true')
        print()
        ev('(display (list 1 2 "Do you see one, two and this in a list?"))')

        self.assertEqual(ev('(= 3 4)'), 'false')
        self.assertEqual(ev('(equal? (list 1 2 3) (list 1 2 3))'), 'true')

        self.assertEqual(ev('(= 1 1 1 1)'), 'true')
        self.assertEqual(ev('(= 1 1 1 2)'), 'false')

        self.assertEqual(ev('(< 1 2 3 4)'), 'true')
        self.assertEqual(ev('(> 4 3 2 1)'), 'true')
        self.assertEqual(ev('(<= 1 2 2 3)'), 'true')
        self.assertEqual(ev('(>= 3 3 2 1)'), 'true')

    def test_define(self):

        ev("""
        (define (fib n)
          (if (< n 2)
              n
              (+ (fib (- n 1)) (fib (- n 2)))))
        """)

        ev("""
        (define (sum n)
          (define (loop n result)
            (if (= n 0)
                result
                (loop (- n 1) (+ n result))))
          (loop n 0))
        """)

        self.assertEqual(ev("(sum 100)"), 5050)
        self.assertEqual(ev("(fib 10)"), 55)

        ev("""
        (define (map fn xs)
          (if (null? xs)
              '()
              (cons (fn (car xs)) (map fn (cdr xs)))))
        """)

        self.assertEqual(ev("(map fib '(1 2 3 4 5 6 7 8))"),
                         ev("(list 1 1 2 3 5 8 13 21)"))



unittest.main()
