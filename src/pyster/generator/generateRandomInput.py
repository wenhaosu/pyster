import inspect
import random


def merge_raw(param_type: str):
    merge_funcs = {
        "string": lambda x: ''.join([chr(val) for val in x]),
        "int": lambda x: int(''.join([str(val) for val in x])),
        "bool": lambda x: True if x[0] == 0 else False
    }
    return merge_funcs[param_type]


def generate_random_value(param_type: str):
    choices = range(0, 10)
    value_length = random.randint(1, 32)
    if param_type == 'string':
        choices = range(ord('a'), ord('z') + 1)
    elif param_type == 'int':
        value_length = random.randint(1, 9)
    elif param_type == 'bool':
        choices = range(2)
        value_length = 1
    else:
        raise Exception("Type not defined for " + param_type)

    return merge_raw(param_type)(random.choices(choices, k=value_length))


class TestCase(object):
    def __init__(self, class_init: any, func_sig: any):
        self.class_init = class_init
        self.target_func_sig = func_sig

    def generate_random_test(self) -> dict:
        arg_arr = []
        sig = repr(inspect.signature(self.target_func_sig[1]))
        sig_vec = sig[sig.index('(') + 1: sig.index(')')].split(', ')

        for param in sig_vec:
            if param == 'self':
                continue
            idx = param.find(':')
            if idx == -1:
                raise Exception("Type of parameter not defined")
            param_type = param[idx + 1:].strip()
            arg_arr.append(generate_random_value(param_type))

        class_item = self.class_init()
        ret_val = getattr(class_item, self.target_func_sig[0])(*arg_arr)

        return {'args': arg_arr, 'ret': ret_val}
