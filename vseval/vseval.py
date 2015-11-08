__all__ = ['vseval', 'Env', 'UnboundVar', 'GLOBAL_ENV']


from collections import namedtuple



class LispException(Exception): pass
class UnboundVar(LispException): pass

compound_procedure = namedtuple('compound_procedure', 'params, body, env')


def vseval(exp, env):
    # properly tail recursive
    while True:
        if is_self_evaluating(exp):
            return exp
        # exp is a variable
        if isinstance(exp, str):
            return env.lookup(exp)

        cmd, *args = exp

        if cmd == 'quote':
            return text_of_quotation(exp, env)
        if cmd == 'set!':
            return env.assign(exp)
        if cmd == 'define':
            return env.define(to_lambda(exp))
        if cmd == 'if':
            test, yes, no = args
            exp = yes if vseval(test, env) != 'false' else no
            continue
        if cmd == 'lambda':
            params, *body = args
            # attach 'begin' if body contains multiple actions
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
    """number, string, booleans
    """
    return \
        isinstance(exp, int) or isinstance(exp, float) \
        or (isinstance(exp, str) and len(exp) >=2 and exp[0] == '"' and exp[-1] == '"') \
        or exp == 'true' or exp == 'false'


def text_of_quotation(exp, env):
    """ '(1 a) => (list '1 'a) and evaluate
    """
    _, text = exp
    if isinstance(text, list):
        return vseval(["list"] + [['quote', x] for x in text], env)
    return text


def to_lambda(exp):
    "(define (foo x) ...) => (define foo (lambda (x) ...))"
    _, var, *body = exp
    if isinstance(var, list):
        name, *params = var
        return ['define', name, ['lambda', params] + body]
    return exp


class Env:
    def __init__(self, frame={}):
        self.frame = frame
        # Upper Env, not upper frame
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
        # evaluate the value expression first before the assignment
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


def setup_global_env():
    import operator
    from functools import reduce

    class cons(namedtuple('cons', 'car, cdr')):
        __slots__ = ()
        def __str__(self):
            elts = [str(self.car)]
            cdr = self.cdr

            while isinstance(cdr, cons):
                elts.append(str(cdr.car))
                cdr = cdr.cdr
            if cdr != []:
                elts.append('.')
                elts.append(str(cdr))
            return '(' + ' '.join(elts) + ')'

    def lisp_list(*args):
        args = list(args)
        result = []
        while args:
            result = cons(args.pop(), result)
        return result

    def lisp_compare(xs, pred):
        for x1, x2 in zip(xs, xs[1:]):
            if not pred(x1, x2):
                return 'false'
        return 'true'

    frame = GLOBAL_ENV.frame

    frame['+'] = lambda *xs: sum(xs)
    frame['-'] = lambda *xs: reduce(lambda x, y: x - y, xs)
    frame['*'] = lambda *xs: reduce(lambda x, y: x * y, xs)
    frame['/'] = lambda *xs: reduce(lambda x, y: x / y, xs)
    frame['rem'] = lambda a, b: a % b

    frame['null?'] = lambda x: 'true' if x == [] else 'false'
    frame['cons'] = cons
    frame['car'] = lambda x: x.car
    frame['cdr'] = lambda x: x.cdr
    frame['list'] = lisp_list

    frame['not'] = lambda x: 'true' if not x else 'false'
    frame['='] = lambda *xs: lisp_compare(xs, operator.eq)
    frame['equal?'] = lambda *xs: lisp_compare(xs, operator.eq)
    frame['<'] = lambda *xs: lisp_compare(xs, operator.lt)
    frame['>'] = lambda *xs: lisp_compare(xs, operator.gt)
    frame['<='] = lambda *xs: lisp_compare(xs, operator.le)
    frame['>='] = lambda *xs: lisp_compare(xs, operator.ge)

    frame['display'] = print


GLOBAL_ENV = Env()
setup_global_env()
