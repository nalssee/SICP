from lisp_parser import parse
import pprint


def lisp_eval(expr):
    return expr


if __name__ == "__main__":

    print("""
    SICP LISP!!
    Happy Hacking
    """)

    while True:
        print("lisp> ", end='')
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
            pprint.pprint(lisp_eval(expr))

        except Exception as e:
            print(e)
