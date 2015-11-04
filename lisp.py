from lisp_parser import parse


def evaluate(exp, env):
    if is_self_evaluating(exp):
        return exp
    if is_variable(exp):
        return lookup_variable_value(exp, env)
    if is_tagged(exp, 'quote'):
        return text_of_quotation(exp)
    if is_tagged(exp, 'set!'):
        return eval_assignment(exp, env)
    if is_tagged(exp, 'define'):
        return eval_definition(exp, env)
    if is_tagged(exp, 'if'):
        return eval_if(exp, env)
    if is_tagged(exp, 'lambda'):
        return make_procedure(lambda_parameters(exp),
                              lambda_body(exp),
                              env)
    if is_tagged(exp, 'begin'):
        return eval_sequence(begin_actions(exp), env)
    if is_tagged(exp, 'cond'):
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
