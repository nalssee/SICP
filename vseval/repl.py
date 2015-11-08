import os
import sys

FILEPATH = os.path.dirname(os.path.realpath(__file__))
PYPATH = os.path.join(FILEPATH, '..', '..')
sys.path.append(PYPATH)

from SICP.vseval.vseval import *
from SICP.vseval.parser import parse


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
