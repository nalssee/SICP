""" A simple lisp parser for SICP exercises

Mostly from norvig.com,
just using a coroutine instead of lists.
"""
import re

__all__ = ["parse"]

SPECIEAL_TOKENS = {"'": 'quote',
                   ".": 'dot',}

def tokenize(expr):
    regex = re.compile("""(
    '|                        # quote
    \(|                       # left paren
    \)|                       # right paren
    [\w.?!+-></=*+]+|         # identifier
    ".*?"|                    # string
    \.
    )
    """, re.VERBOSE)
    return (x for x in re.findall(regex, expr) if x != '')


def parse(expr):
    reader = token_reader()
    reader.send(None)
    try:
        for token in tokenize(expr):
            reader.send(token)
    except StopIteration as e:
        return e.value


def token_reader():
    """Consume tokens to construct a lisp expression
    """
    token = yield
    if token == '(':
        parsed_expr = []
        while True:
            exp1 = yield from token_reader()
            if exp1 == ')': return parsed_expr
            # dotted expression must be the last one in a list
            if is_dotted(exp1):
                if (yield from token_reader()) == ')':
                    return parsed_expr + [exp1]
                raise ValueError('Invalid dot expression')

            parsed_expr.append(exp1)
    # quote and dot may not be necessary for the register machine simulator.
    elif token in SPECIEAL_TOKENS:
        return [SPECIEAL_TOKENS[token], (yield from token_reader())]

    return atom(token)


def atom(token):
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError: return token


def is_dotted(exp):
    return isinstance(exp, list) \
        and len(exp) == 2 \
        and exp[0] == SPECIEAL_TOKENS['.']
