__all__ = ['vseval', 'Env', 'UnboundVar', 'GLOBAL_ENV']


from collections import namedtuple
from SICP.vseval.parser import parse
from SICP.vseval.builtins import *

compound_procedure = namedtuple('compound_procedure', 'params, body, env')

def vseval(exp, env):
    # properly tail recursive
    while True:
        if is_self_evaluating(exp):
            return exp
        if isinstance(exp, str):
            return env.lookup(exp)

        cmd, *args = exp

        if cmd == 'quote':
            return text_of_quotation(exp, env)
        if cmd == 'set!':
            return env.assign(exp)
        if cmd == 'define':
            return env.define(paren2lambda(exp))
        if cmd == 'if':
            test, yes, no = args
            exp = yes if vseval(test, env) != 'false' else no
            continue
        if cmd == 'lambda':
            params, *body = args
            body = body[0] if len(body) == 1 else ['begin'] + body
            return compound_procedure(params, body, env)
        if cmd == 'begin':
            *actions, exp = args
            for act in actions:
                vseval(act, env)
            continue
        # And it's a procedure application
        proc = vseval(cmd, env)
        args = [vseval(arg, env) for arg in args]

        if isinstance(proc, compound_procedure):
            env = proc.env.extend(proc.params, args)
            exp = proc.body
            continue
        return proc(*args)


def is_self_evaluating(exp):
    return \
        isinstance(exp, int) or isinstance(exp, float) \
        or (isinstance(exp, str) and len(exp) >=2 and exp[0] == '"' and exp[-1] == '"') \
        or exp == 'true' or exp == 'false'


def text_of_quotation(exp, env):
    _, text = exp
    if isinstance(text, list):
        return vseval(["list"] + [['quote', x] for x in text], env)
    return text


class Env:
    def __init__(self, frame={}):
        self.frame = frame
        # Upper Env
        self.upper = None

    def lookup(self, var):
        try:
            return self.frame[var]
        except KeyError:
            upper_env = self.upper
            if upper_env == None:
                raise UnboundVar(var)
            return upper_env.lookup(var)

    def assign(self, exp):
        _, var, valexp = exp
        # evaluate first before the assignment
        val = vseval(valexp, self)
        def env_loop(env):
            try:
                env.frame[var]
            except KeyError:
                upper_env = env.upper
                if upper_env == None:
                    raise UnboundVar(var)
                env_loop(upper_env)
            # var exists at this point
            else:
                env.frame[var] = val
        env_loop(self)

    def define(self, exp):
        _, var, val = exp
        self.frame[var] = vseval(val, self)

    def extend(self, params, args):
        newframe = {}
        for p, a in zip(params, args):
            newframe[p] = a
        newenv = Env(newframe)
        newenv.upper = self
        return newenv


class LispException(Exception): pass
class UnboundVar(LispException): pass


def paren2lambda(exp):
    "(define (foo x) ...) => (define foo (lambda (x) ...))"
    _, var, *body = exp
    if isinstance(var, list):
        name, *params = var
        return ['define', name, ['lambda', params] + body]
    return exp


def setup_global_env():
    frame = GLOBAL_ENV.frame

    frame['+'] = plus
    frame['-'] = minus
    frame['*'] = mult
    frame['/'] = div
    frame['rem'] = lisp_rem

    frame['null?'] = is_null
    frame['cons'] = cons
    frame['car'] = car
    frame['cdr'] = cdr
    frame['list'] = lisp_list

    frame['not'] = lisp_not
    frame['='] = lisp_eq
    frame['equal?'] = lisp_eq
    frame['<'] = lisp_lt
    frame['>'] = lisp_gt
    frame['<='] = lisp_le
    frame['>='] = lisp_ge

    frame['display'] = print


GLOBAL_ENV = Env()
setup_global_env()
