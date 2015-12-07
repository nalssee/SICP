class Machine:
    def __init__(self, register_names, ops, controller_text):
        self.pc = Register()
        self.flag = Register()
        self.stack = Stack()
        self.ops = {'initialize': (lambda : self.stack.__init__())}
        self.register_table = {'pc': self.pc, 'flag': self.flag}

        for name in register_names:
            self.allocate_register(name)
        for op_name, op_fn in ops:
            self.ops[op_name] = op_fn
        self.pc.value = assemble(controller_text, self)

    def allocate_register(self, name):
        if name in self.register_table:
            raise NameError('Regiser already exists')
        self.register_table[name] = Register()

    def get_register(self, name):
        return self.register_table[name]

    def start(self):
        while True:
            insts = self.pc.value
            if not insts: return
            insts[0].proc()


class Stack:
    def __init__(self):
        self.values = []
    def push(self, value):
        self.values.append(value)
    def pop(self):
        return self.values.pop()


class Register:
    def __init__(self, value=False):
        self.value = value


class Inst:
    "Instruction"
    def __init__(self, text, proc=False):
        self.text = text
        self.proc = proc


def extract_labels(ast):
    def remove_labels(xs):
        return [x for x in xs if not isinstance(x, str)]

    insts = [(x if isinstance(x, str) else Inst(x)) for x in ast]
    labels = {}
    for i, inst in enumerate(insts):
        if isinstance(inst, str):
            labels[inst] = remove_labels(insts[i + 1:])
    return remove_labels(insts), labels


def assemble(ast, machine):
    insts, labels = extract_labels(ast)
    pc = machine.get_register("pc")
    flag = machine.get_register("flag")
    stack = machine.stack
    ops = machine.ops
    for inst in insts:
        inst.proc = make_exec_proc(inst.text, labels, machine, pc, flag, stack, ops)
    return insts


def make_exec_proc(inst, labels, machine, pc, flag, stack, ops):
    if inst[0] == 'assign':
        return make_assign(inst, machine, labels, ops, pc)
    if inst[0] == 'test':
        return make_test(inst, machine, labels, ops, flag, pc)
    if inst[0] == 'branch':
        return make_branch(inst, machine, labels, flag, pc)
    if inst[0] == 'goto':
        return make_goto(inst, machine, labels, pc)
    if inst[0] == 'save':
        return make_save(inst, machine, stack, pc)
    if inst[0] == 'restore':
        return make_restore(inst, machine, stack, pc)
    if inst[0] == 'perform':
        return make_perform(inst, machine, labels, ops, pc)
    raise ValueError("Unknown command: %s" % (command,))


def make_assign(inst, machine, labels, ops, pc):
    _, reg, *val = inst
    target = machine.get_register(reg)
    value_proc = make_operation_exp(val, machine, labels, ops) \
                 if is_operation_exp(val) \
                    else make_primitive_exp(val[0], machine, labels)
    def thunk():
        target.value = value_proc()
        pc.value = pc.value[1:]
    return thunk


def make_test(inst, machine, labels, ops, flag, pc):
    _, *cond = inst
    if is_operation_exp(cond):
        cond_proc = make_operation_exp(cond, machine, labels, ops)
        def thunk():
            flag.value = cond_proc()
            pc.value = pc.value[1:]
        return thunk
    else:
        raise ValueError("Bad Test expression: %s" % (cond,))


def make_branch(inst, machine, labels, flag, pc):
    _, (tag, dest) = inst
    if tag == 'label':
        insts = labels[dest]
        def thunk():
            if flag.value:
                pc.value = insts
            else:
                pc.value = pc.value[1:]
        return thunk
    else:
        raise ValueError("Bad BRANCH instruction: %s" % (inst,))


def make_goto(inst, machine, labels, pc):
    _, (tag, val) = inst
    if tag == 'label':
        insts = labels[val]
        def thunk(): pc.value = insts
        return thunk

    elif tag == 'reg':
        reg = machine.get_register(val)
        def thunk(): pc.value = reg.value
        return thunk

    else:
        raise ValueError("Bad Goto instruction: %s" % (inst,))


def make_save(inst, machine, stack, pc):
    reg = machine.get_register(inst[1])
    def thunk():
        stack.push(reg.value)
        pc.value = pc.value[1:]
    return thunk


def make_restore(inst, machine, stack, pc):
    reg = machine.get_register(inst[1])
    def thunk():
        reg.value = stack.pop()
        pc.value = pc.value[1:]
    return thunk


def make_perform(inst, machine, lables, ops, pc):
    _, *action = inst
    if is_operation_exp(action):
        action_proc = make_operation_exp(action, machine, labels, ops)
        def thunk():
            action_proc()
            pc.value = pc.value[1:]
        return thunk
    else:
        raise ValueError("Bad PERFROM instruction %s" % (inst,))


def make_primitive_exp(exp, machine, labels):
    tag, val = exp
    if tag == 'const':
        return lambda: val
    elif tag == 'label':
        insts = labels[val]
        return lambda: insts
    elif tag == 'reg':
        reg = machine.get_register(val)
        return lambda: reg.value
    else:
        raise ValueError('Unknown expression type %s' % (exp,))


def make_operation_exp(exp, machine, labels, ops):
    (_, op_name), *args = exp
    op = ops[op_name]
    aprocs = [make_primitive_exp(arg, machine, labels) for arg in args]
    return lambda: op(*[p() for p in aprocs])


def is_operation_exp(exp):
    try:
        (cmd, _), *_ = exp
        return cmd == 'op'
    except:
        return False
