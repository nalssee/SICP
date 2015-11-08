import os
import sys

TESTPATH = os.path.dirname(os.path.realpath(__file__))
PYPATH = os.path.join(TESTPATH, '..', '..')
sys.path.append(PYPATH)

print(PYPATH)

from SICP.vseval.parser import parse
from SICP.vseval.vseval import *


PROMPT = "VSEVAL> "

print("""
Vanilla Scheme interpreter for SICP Chapter 4

After typing in a Lisp expression,
press Enter followed by ctrl-d for evaluation.

(quit) or (exit) to finish this repl.
""")

while True:
    print(PROMPT, end='')
    code_all = []
    try:
        while True:
            try:
                code = input()
                code_all.append(code)
            except EOFError:
                break
        expr = parse(' '.join(code_all))
        if expr == ['quit'] or expr == ['exit']:
            print("Goodbye!!")
            break
        print("=> ", end='')
        print(vseval(expr, GLOBAL_ENV))

    except Exception as e:
        print(e)
