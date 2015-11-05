__all__ = ['evaluate', 'Env', 'UnboundVar']

from .lisp_parser import parse


def evaluate(exp, env):
    if is_self_evaluating(exp):
        return exp
    if is_variable(exp):
        return env.lookup(exp)
    if tagged(exp, 'quote'):
        return text_of_quotation(exp)
    if tagged(exp, 'set!'):
        return env.assign(exp)
    if tagged(exp, 'define'):
        return eval_definition(exp, env)
    if tagged(exp, 'if'):
        return eval_if(exp, env)
    if tagged(exp, 'lambda'):
        return make_procedure(lambda_parameters(exp),
                              lambda_body(exp),
                              env)
    if tagged(exp, 'begin'):
        return eval_sequence(begin_actions(exp), env)
    if tagged(exp, 'cond'):
        return evaluate(cond2if(exp), env)
    if is_application(exp):
        return apply(evaluate(operator(exp), env),
                     list_of_values(operands(exp), env))
    raise ValueError('Unknown expression', exp)


def apply(proc, args):
    if is_primitive(proc):
        return apply_primitive_proc(proc, args)
    if is_compound_proc(proc):
        return eval_sequence(proc_body(proc),
                             extend_env(proc_params(proc),
                                        args,
                                        proc_env(proc)))
    raise ValueError('Unknown proc type', proc)


def is_self_evaluating(exp):
    return isinstance(exp, int) or isinstance(exp, float) \
        or (isinstance(exp, str) and len(exp) >=2 and exp[0] == '"' and exp[-1] == '"')


def is_variable(exp):
    return isinstance(exp, str)


def tagged(exp, command):
    return isinstance(exp, list) and exp != [] and exp[0] == command


def is_application(exp):
    return isinstance(exp, list) and exp != []


class Env:
    def __init__(self, frame={}):
        self.frame = frame
        # Upper frame
        self.upper = None

    def lookup(self, var):
        try:
            return self.frame[var]
        except KeyError:
            upperframe = self.upper
            if upperframe == None:
                raise UnboundVar(var)
            return upperframe.lookup(var)

    def assign(self, exp):
        self.frame[exp[1]] = evaluate(exp[2], self)


class LispException(Exception):
    pass


class UnboundVar(LispException):
    pass


def text_of_quotation(exp):
    return exp[1]
