import unittest
from SICP.rms.parser import parse
from SICP.rms.rms import *


class RMSTest(unittest.TestCase):
    def test_gcd(self):
        code = """
        (test-b
          (test (op =) (reg b) (const 0))
          (branch (label gcd-done))
          (assign t (op rem) (reg a) (reg b))
          (assign a (reg b))
          (assign b (reg t))
          (goto (label test-b))
        gcd-done)
        """
        m = Machine(["a", "b", "t"],
                    [("rem", lambda x, y: x % y),
                     ("=", lambda x, y: x == y)],
                    parse(code))
        m.get_register('a').value = 206
        m.get_register('b').value = 40
        m.start()

        self.assertEqual(m.get_register('a').value, 2)

    def test_fib(self):
        code = """
        (fib-start
          (assign continue (label fib-done))
        fib-loop
          (test (op <) (reg n) (const 2))
          (branch (label immediate-answer))
          (save continue)
          (assign continue (label afterfib-n-1))
          (save n)
          (assign n (op -) (reg n) (const 1))
          (goto (label fib-loop))
        afterfib-n-1
          (restore n)
          (restore continue)
          (assign n (op -) (reg n) (const 2))
          (save continue)
          (assign continue (label afterfib-n-2))
          (save val)
          (goto (label fib-loop))
        afterfib-n-2
          (assign n (reg val))
          (restore val)
          (restore continue)
          (assign val (op +) (reg val) (reg n))
          (goto (reg continue))
        immediate-answer
          (assign val (reg n))
          (goto (reg continue))
        fib-done)
        """
        m = Machine(['n', 'val', 'continue'],
                    [('<', lambda a, b: a < b),
                     ('-', lambda a, b: a - b),
                     ('+', lambda a, b: a + b)],
                    parse(code))
        m.get_register('n').value = 10
        m.start()
        self.assertEqual(m.get_register('val').value, 55)


if __name__ == "__main__":
    unittest.main()
