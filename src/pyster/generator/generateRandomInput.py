import inspect
import random


def merge_raw(param_type: str):
    merge_funcs = {
        "str": lambda x: ''.join([chr(val) for val in x]),
        "int": lambda x: int(''.join([str(val) for val in x])),
        "bool": lambda x: True if x[0] == 0 else False
    }
    return merge_funcs[param_type]


def generate_random_value(param_type: str):
    choices = range(0, 10)
    value_length = random.randint(1, 32)
    if param_type == 'str':
        choices = range(ord('a'), ord('z') + 1)
    elif param_type == 'int':
        value_length = random.randint(1, 9)
    elif param_type == 'bool':
        choices = range(2)
        value_length = 1
    else:
        raise Exception("Type not defined for:" + param_type + ':')

    return merge_raw(param_type)(random.choices(choices, k=value_length))


def extract_sig_vec(sig_obj: any):
    sig = repr(inspect.signature(sig_obj[1]))
    # Do not return 'self' in sig vec
    return sig[sig.index('(') + 1: sig.index(')')].split(', ')[1:]


def convert_arg_type(param_type: str, param: str):
    if param_type == 'str':
        return param
    if param_type == 'int':
        return int(param)
    if param_type == 'bool':
        return param == 'True'


def fill_param_array(sig_vec: any):
    arr = []
    for param in sig_vec:
        idx = param.find(':')
        if idx == -1:
            raise Exception("Type of parameter not defined")
        param_type = param[idx + 1:].strip()
        idx = param_type.find('=')
        if idx == -1:
            arr.append(generate_random_value(param_type))
        else:
            # When we have a default value for an argument,
            # there's 50% chance to directly use that argument
            default_val = param_type[idx + 1:].strip()
            param_type = param_type[:idx].strip()
            if random.choice([True, False]):
                arr.append(generate_random_value(param_type))
            else:
                arr.append(convert_arg_type(param_type, default_val))
    return arr


class TestCase(object):
    def __init__(self, class_init: any, init_sig: any, func_sig: any):
        self.class_init = class_init
        self.target_func_sig = func_sig
        self.init_sig_vec = extract_sig_vec(init_sig)
        self.func_sig_vec = extract_sig_vec(func_sig)

    def generate_random_test(self) -> dict:
        init_arr = fill_param_array(self.init_sig_vec)
        arg_arr = fill_param_array(self.func_sig_vec)

        class_item = self.class_init(*init_arr)
        ret_val = getattr(class_item, self.target_func_sig[0])(*arg_arr)

        return {'init_args': init_arr, 'func_args': arg_arr, 'ret': ret_val}
