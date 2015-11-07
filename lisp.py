__all__ = ['evaluate', 'Env', 'UnboundVar', 'GLOBAL_ENV']


from collections import namedtuple
from SICP.lisp_parser import parse
from SICP.builtins import *

compound_procedure = namedtuple('compound_procedure', 'params, body, env')

def evaluate(exp, env):
    while True:
        if is_self_evaluating(exp):
            return exp
        if is_variable(exp):
            return env.lookup(exp)
        if tagged(exp, 'quote'):
            return text_of_quotation(exp, env)
        if tagged(exp, 'set!'):
            return env.assign(exp)
        if tagged(exp, 'define'):
            return env.define(paren2lambda(exp))
        if tagged(exp, 'if'):
            _, test, yes, no = exp
            exp = yes if evaluate(test, env) != 'false' else no
            continue
        if tagged(exp, 'lambda'):
            _, params, *body = exp
            body = body[0] if len(body) == 1 else ['begin'] + body
            return compound_procedure(params, body, env)
        if tagged(exp, 'begin'):
            _, *actions, exp = exp
            for act in actions:
                evaluate(act, env)
            continue
        # And it's a procedure application
        op, *args = exp
        proc = evaluate(op, env)
        args = [evaluate(arg, env) for arg in args]

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
        return evaluate(["list"] + [['quote', x] for x in text], env)
    return text


def is_variable(exp):
    return isinstance(exp, str)


def tagged(exp, command):
    return isinstance(exp, list) and exp != [] and exp[0] == command


def is_application(exp):
    return isinstance(exp, list) and exp != []


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
        val = evaluate(valexp, self)
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
        self.frame[var] = evaluate(val, self)

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
    def assign_pyfunc(func_symb, pyfunc):
        frame = GLOBAL_ENV.frame
        frame[func_symb] = pyfunc

    assign_pyfunc('+', plus)
    assign_pyfunc('-', minus)
    assign_pyfunc('*', mult)
    assign_pyfunc('/', div)
    assign_pyfunc('rem', lisp_rem)

    assign_pyfunc('null?', is_null)
    assign_pyfunc('cons', cons)
    assign_pyfunc('car', car)
    assign_pyfunc('cdr', cdr)
    assign_pyfunc('list', lisp_list)

    assign_pyfunc('not', lisp_not)
    assign_pyfunc('=', lisp_eq)
    assign_pyfunc('equal?', lisp_eq)
    assign_pyfunc('<', lisp_lt)
    assign_pyfunc('>', lisp_gt)
    assign_pyfunc('<=', lisp_le)
    assign_pyfunc('>=', lisp_ge)

    assign_pyfunc('display', print)


GLOBAL_ENV = Env()
setup_global_env()
