import random
import string
import sys
import os
import importlib
from inspect import Parameter

from ..common import ConfigObject, is_primitive, indent


def gen_str(value):
    if isinstance(value, Parameter):
        return value.name
    if isinstance(value, str):
        return 'r' + '"' + value + '"'
    if isinstance(value, list):
        return "[" + ", ".join([gen_str(i) for i in value]) + "]"
    return str(value)


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
        def parse(args, lookup_dict):
            init_args = []
            for arg in args:
                if isinstance(arg, Parameter):
                    init_args.append(lookup_dict[arg.name])
                elif isinstance(arg, list):
                    init_args.append(parse(arg, lookup_dict))
                else:
                    init_args.append(arg)
            if (self.func_name in ["_str()", "__repr__", "__unicode__"]):
                print(self.func_name)
                print(init_args)
            return init_args

        def run_prepare(obj_names, obj_dict):
            instance_dict = {}
            for obj_name in obj_names:
                class_name = obj_dict[obj_name]['class']
                module_name = obj_dict[obj_name]['module']
                module_obj = importlib.import_module(module_name)
                class_obj = getattr(module_obj, class_name)
                _init_args = parse(obj_dict[obj_name]['args'], instance_dict)
                instance_dict[obj_name] = class_obj(*_init_args)
            return instance_dict

        [obj_names, obj_dict, arg_list] = self.init_list
        instance_dict = run_prepare(obj_names, obj_dict)
        call_args = parse(arg_list, instance_dict)
        target_instance = self.target_class(*call_args)

        target_func = getattr(target_instance, self.func_name)

        [obj_names, obj_dict, arg_list] = self.arg_list
        instance_dict = run_prepare(obj_names, obj_dict)
        call_args = parse(arg_list, instance_dict)

        self.ret = target_func(*call_args)
        print(self.ret)
        self.valid = True


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
            call_code += ', '.join([gen_str(arg) for arg in args])
            call_code += ')'
            assert_code = "assert "
            if is_primitive(ret):
                assert_code += call_code
                if isinstance(ret, bool):
                    assert_code += " is "
                else:
                    assert_code += " == "
                assert_code += gen_str(ret)
            elif ret is None:
                assert_code += call_code
                assert_code += " is None"
            else:
                if hasattr(ret, '__module__'):
                    assert_code += "isinstance({}, {})".format(call_code,
                                                           ret.__module__ + '.' + type(ret).__name__)
                else:
                    assert_code += "{} is not None".format(call_code)
                
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
