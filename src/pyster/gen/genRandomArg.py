import random
import string
import sys
import os
import importlib
from inspect import Parameter

from ..common import ConfigObject, is_primitive, indent


def gen_str(value):
    if isinstance(value, str):
        return "'" + value + "'"
    return str(value)


def check_primitive(value):
    return value in ['int', 'str', 'bool', 'float']


def gen_random_primitive(arg_type: str, arg_len=10):
    if arg_type == 'int':
        if random.randint(1, 10) <= 3:
            return 0
        return random.randint(0, 10 ** arg_len)
    elif arg_type == 'str':
        if random.randint(1, 10) <= 3:
            return ""
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for _ in range(arg_len))
    elif arg_type == 'bool':
        return bool(random.getrandbits(1))
    elif arg_type == 'float':
        if random.randint(1, 10) <= 3:
            return 0
        return random.uniform(0, 10 ** (arg_len / 2))
    else:
        return None


class FuncTest(object):
    def __init__(self, config: ConfigObject, func_info: list):
        [module_name, class_name, func_name] = func_info
        self.func_name = func_name
        self.class_name = class_name
        self.config = config
        self.func_args = config.config[module_name][class_name][func_name]
        self.init_args = config.config[module_name][class_name]["__init__"]
        self.cnt = 0

    def gen_arg(self, arg_type: str, default_val, obj_names, obj_dict):
        # 30% to directly use default value
        if random.randint(1, 10) <= 3 and default_val != '':
            return default_val
        # 70% to automatically generate
        if check_primitive(arg_type):
            return gen_random_primitive(arg_type)
        elif arg_type == 'dict':
            if random.randint(1, 10) <= 3:
                return {}
            return default_val
        elif arg_type == 'list':
            return self.gen_list(default_val, obj_names, obj_dict)
        elif arg_type == 'any':
            return None if default_val == "" else default_val
        else:
            return self.gen_defined_type(arg_type, obj_names, obj_dict)

    def gen_defined_type(self, arg_type: str, obj_names, obj_dict):
        arg_name = 'arg_' + str(self.cnt)
        self.cnt += 1
        arg_obj = Parameter(arg_name, Parameter.KEYWORD_ONLY)
        obj_names[:0] = [arg_name]
        for mod, temp in self.config.config.items():
            for key, val in temp.items():
                if key == arg_type:
                    obj_dict[arg_name] = {
                        'module': mod,
                        'class': arg_type,
                        'args': self.gen_list(val['__init__'], obj_names,
                                              obj_dict)}
        return arg_obj

    def gen_list(self, list_args: list, obj_names, obj_dict):
        args_list = []
        for arg in list_args:
            if 'self' in arg.keys():
                continue
            arg_type, default_val = random.choice(list(arg.items()))
            args_list.append(
                self.gen_arg(arg_type, default_val, obj_names, obj_dict))
        return args_list

    def generate_random_test(self):
        obj_names = []
        obj_dict = {}
        arg_list = self.gen_list(self.func_args, obj_names, obj_dict)

        init_obj_names = []
        init_obj_dict = {}
        init_arg_list = self.gen_list(self.init_args, init_obj_names,
                                      init_obj_dict)

        return {
            "func_name": self.func_name,
            "class_name": self.class_name,
            "init_list": [init_obj_names, init_obj_dict, init_arg_list],
            "arg_list": [obj_names, obj_dict, arg_list]
        }


class UnitTest(object):
    def __init__(self, test_info: dict, config: ConfigObject):
        self.class_name = test_info['class_name']
        self.func_name = test_info['func_name']
        self.init_list = test_info['init_list']
        self.arg_list = test_info['arg_list']

        self.ret = None
        self.exception = None

        self.valid = False

        self.module_name = config.module_name
        self.project_path = config.project_path
        self.import_modules = list(config.config.keys())

        sys.path.insert(0, self.project_path)

        self.test_module = importlib.import_module(self.module_name)
        self.target_class = getattr(self.test_module, self.class_name)

        self.output = []

    def run(self):
        def run_prepare(obj_names, obj_dict):
            instance_dict = {}
            for obj_name in obj_names:
                class_name = obj_dict[obj_name]['class']
                module_name = obj_dict[obj_name]['module']
                module_obj = importlib.import_module(module_name)
                class_obj = getattr(module_obj, class_name)
                init_args = []
                for arg in obj_dict[obj_name]['args']:
                    if isinstance(arg, Parameter):
                        init_args.append(instance_dict[arg.name])
                    else:
                        init_args.append(arg)
                instance_dict[obj_name] = class_obj(*init_args)
            return instance_dict
        
        self.valid = true

        [obj_names, obj_dict, arg_list] = self.init_list

        instance_dict = run_prepare(obj_names, obj_dict)

        call_args = []
        for arg in arg_list:
            if isinstance(arg, Parameter):
                call_args.append(instance_dict[arg.name])
            else:
                call_args.append(arg)

        target_instance = self.target_class(*call_args)

        target_func = getattr(target_instance, self.func_name)

        [obj_names, obj_dict, arg_list] = self.arg_list
        instance_dict = run_prepare(obj_names, obj_dict)
        call_args = []
        for arg in arg_list:
            if isinstance(arg, Parameter):
                call_args.append(instance_dict[arg.name])
            else:
                call_args.append(arg)

        self.ret = target_func(*call_args)

        print(self.ret)


    def dump(self):
        if not self.valid:
            return

        def dump_init(var_name, class_name, args):
            init_code = var_name + ' = ' + class_name + '('
            init_code += ','.join([gen_str(arg) for arg in args])
            init_code += ')'
            self.output.append(indent(1) + init_code)

        def dump_assert(function_name, args, ret):
            call_code = "var." + function_name + '('
            call_code += ','.join([gen_str(arg) for arg in args])
            call_code += ')'
            assert_code = "assert "
            if is_primitive(ret):
                assert_code += call_code
                assert_code += " == "
                assert_code += gen_str(ret)
            elif ret is None:
                assert_code += call_code
                assert_code += " is None"
            else:
                assert_code += "isinstance({}, {})".format(call_code,
                                                           ret.__module__ + '.' + type(ret).__name__)
            self.output.append(indent(1) + assert_code)

        def init_prepare(obj_names, obj_dict):
            for obj_name in obj_names:
                class_name = obj_dict[obj_name]['class']
                module_name = obj_dict[obj_name]['module']
                args = obj_dict[obj_name]['args']
                dump_init(obj_name, module_name + '.' + class_name, args)

        [obj_names, obj_dict, arg_list] = self.init_list
        init_prepare(obj_names, obj_dict)
        dump_init("var", self.module_name + '.' + self.class_name, arg_list)

        if self.func_name == "__init__":
            assert_code = "assert isinstance(var, {}.{})".format(
                self.module_name, self.class_name)
            self.output.append(indent(1) + assert_code)
            return

        [obj_names, obj_dict, arg_list] = self.arg_list
        init_prepare(obj_names, obj_dict)
        dump_assert(self.func_name, arg_list, self.ret)
