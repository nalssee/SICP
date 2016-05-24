def is_self_evaluating(exp):
    """number, string, booleans
    """
    return \
        isinstance(exp, int) or isinstance(exp, float) \
        or (isinstance(exp, str) and len(exp) >= 2 and exp[0] == '"' and exp[-1] == '"') \
        or exp == 'true' or exp == 'false'


def text_of_quotation(exp):
    pass
