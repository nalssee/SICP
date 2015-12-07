import os
import sys


from SICP.lisp_parser.lp import parse
from SICP.vanilla_scheme.vseval import *


PROMPT = "VSEVAL> "

print("""
    Vanilla Scheme interpreter for SICP Chapter 4
    ctrl-d to exit,
    Happy Hacking!!
""")


code_to_eval = []
while True:
    if code_to_eval == []:
        print(PROMPT, end='')
    try:
        code = input()
    except EOFError:
        print('Goodbye!!')
        break
    else:
        code_to_eval.append(code)
        expr = parse(' '.join(code_to_eval))
        # succeeds to parse
        if expr != None:
            try:
                value = vseval(expr, GLOBAL_ENV)
            except UnboundVar as e:
                print('Unbound Variable: ', e)
            except Exception as e:
                print('Error: ', e)
            else:
                print("=> ", end='')
                print(value)
            finally:
                code_to_eval = []
