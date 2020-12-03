import sys
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
            if self.func_name in ["_str()", "__repr__", "__unicode__"]:
                print(self.func_name)
                print(init_args)
            return init_args

        def run_prepare(_obj_names, _obj_dict):
            _instance_dict = {}
            for obj_name in _obj_names:
                class_name = _obj_dict[obj_name]['class']
                module_name = _obj_dict[obj_name]['module']
                module_obj = importlib.import_module(module_name)
                class_obj = getattr(module_obj, class_name)
                _init_args = parse(_obj_dict[obj_name]['args'], _instance_dict)
                _instance_dict[obj_name] = class_obj(*_init_args)
            return _instance_dict

        self.valid = True

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

    def dump(self):
        if not self.valid:
            return

        def dump_init(var_name, class_name, args, _init_indent=1):
            init_code = var_name + ' = ' + class_name + '('
            init_code += ','.join([gen_str(arg) for arg in args])
            init_code += ')'
            self.output.append(indent(_init_indent) + init_code)

        def dump_assert(function_name, args, ret):
            call_code = "var." + function_name + '('
            call_code += ', '.join([gen_str(arg) for arg in args])
            call_code += ')'
            _assert_code = "assert "
            if is_primitive(ret):
                _assert_code += call_code
                if isinstance(ret, bool):
                    _assert_code += " is "
                else:
                    _assert_code += " == "
                _assert_code += gen_str(ret)
            elif ret is None:
                _assert_code += call_code
                _assert_code += " is None"
            else:
                if hasattr(ret, '__module__'):
                    _assert_code += "isinstance({}, {})". \
                        format(call_code,
                               ret.__module__ + '.' + type(ret).__name__)
                else:
                    _assert_code += "{} is not None".format(call_code)

            self.output.append(indent(1) + _assert_code)

        def init_prepare(_obj_names, _obj_dict):
            for obj_name in _obj_names:
                class_name = _obj_dict[obj_name]['class']
                module_name = _obj_dict[obj_name]['module']
                args = _obj_dict[obj_name]['args']
                dump_init(obj_name, module_name + '.' + class_name, args)

        [obj_names, obj_dict, arg_list] = self.init_list
        init_prepare(obj_names, obj_dict)

        init_indent = 1
        if self.exception:
            init_indent += 1
            self.output.append(indent(1) + "try:")
            dump_init("var", self.module_name + '.' + self.class_name,
                      arg_list, init_indent)
            self.output.append(indent(1) + "except Exception as e:")
            self.output.append(indent(2) + "assert isinstance(e, {})".format(
                self.exception.__class__.__name__))
            return

        dump_init("var", self.module_name + '.' + self.class_name, arg_list,
                  init_indent)

        if self.func_name == "__init__":
            assert_code = "assert isinstance(var, {}.{})".format(
                self.module_name, self.class_name)
            self.output.append(indent(1) + assert_code)
            return

        [obj_names, obj_dict, arg_list] = self.arg_list
        init_prepare(obj_names, obj_dict)
        dump_assert(self.func_name, arg_list, self.ret)
