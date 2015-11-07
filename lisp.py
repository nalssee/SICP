__all__ = ['evaluate', 'Env', 'UnboundVar', 'UnknownExpr', 'UnknownProcType',
           'GLOBAL_ENV',
]


from collections import namedtuple
from SICP.lisp_parser import parse
from SICP.builtins import *


def evaluate(exp, env):
    if is_self_evaluating(exp):
        return exp
    if is_variable(exp):
        return env.lookup(exp)
    if tagged(exp, 'quote'):
        _, text = exp
        return text
    if tagged(exp, 'set!'):
        return env.assign(exp)
    if tagged(exp, 'define'):
        return env.define(exp)
    if tagged(exp, 'if'):
        return eval_if(exp, env)
    if tagged(exp, 'lambda'):
        _, params, body = exp
        return compound_procedure(params, body, env)
    if tagged(exp, 'begin'):
        _, *actions = exp
        return eval_sequence(actions, env)
    if tagged(exp, 'cond'):
        return evaluate(cond2if(exp), env)
    if is_application(exp):
        op, *args = exp
        proc = evaluate(op, env)
        args = [evaluate(arg, env) for arg in args]
        return apply(proc, args)
    raise UnknownExpr(exp)


def apply(proc, args):
    if isinstance(proc, primitive_procecure):
        return proc.pyfunc(*args)
    if isinstance(proc, compound_procedure):
        new_env = extend_env(proc.params, args, proc.env)
        return eval_sequence(proc.body, new_env)
    raise UnknownProcType(proc)


primitive_procecure = namedtuple('primitive_procedure', 'pyfunc')
compound_procedure = namedtuple('compound_procedure', 'params, body, env')


def is_self_evaluating(exp):
    return \
        isinstance(exp, int) or isinstance(exp, float) \
        or (isinstance(exp, str) and len(exp) >=2 and exp[0] == '"' and exp[-1] == '"') \
        or exp == 'true' or exp == 'false'


def is_variable(exp):
    return isinstance(exp, str)


def tagged(exp, command):
    return isinstance(exp, list) and exp != [] and exp[0] == command


def is_application(exp):
    return isinstance(exp, list) and exp != []


def eval_if(exp, env):
    _, test, yes, no = exp
    if evaluate(test, env) != 'false':
        return evaluate(yes, env)
    return evaluate(no, env)


def eval_sequence(exps, env):
    "Evaluate expressions in order and return the last one"
    *exps, last = exps
    for exp in exps:
        evaluate(exp, env)
    return evaluate(last, env)


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


class LispException(Exception): pass
class UnknownExpr(LispException): pass
class UnknownProcType(LispException): pass
class UnboundVar(LispException): pass


def setup_global_env():
    def assign_pyfunc(func_symb, pyfunc):
        frame = GLOBAL_ENV.frame
        frame[func_symb] = primitive_procecure(pyfunc)

    assign_pyfunc('+', plus)
    assign_pyfunc('-', minus)
    assign_pyfunc('*', mult)
    assign_pyfunc('/', div)

    assign_pyfunc('null?', is_null)
    assign_pyfunc('cons', cons)
    assign_pyfunc('car', car)
    assign_pyfunc('cdr', cdr)
    assign_pyfunc('list', lisp_list)

    assign_pyfunc('not', lisp_not)
    # just for the sake of convenience
    assign_pyfunc('=', lisp_equal)
    assign_pyfunc('equal?', lisp_equal)

    assign_pyfunc('display', print)


GLOBAL_ENV = Env()
setup_global_env()
