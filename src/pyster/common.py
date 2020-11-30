import json
import os
import typing
import sys


def indent(n: int):
    return "\t" * n


class Colors:
    reset = '\033[0m'

    class ColorCode:
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        cyan = '\033[36m'


def notify(msg, color=Colors.reset):
    sys.stderr.write(color + "== " + msg + '\n' + Colors.reset)
    sys.stderr.flush()


primitive = (int, str, bool, float)
primitive_str = ['int', 'str', 'bool', 'float']


def is_primitive(value):
    if type(value) == str:
        if value in primitive_str:
            return True
    return isinstance(value, primitive)


def assign_type(config_dict, value):
    config_dict.pop('any', None)
    if isinstance(value, dict):
        config_dict['dict'] = value
    elif isinstance(value, list):
        config_dict['list'] = []
        for item in value:
            config_dict['list'].append(dict())
            assign_type(config_dict['list'][-1], item)
    elif is_primitive(value):
        config_dict[type(value).__name__] = value
    else:
        config_dict[type(value).__name__] = ""


class ConfigObject(object):
    def __init__(self, project_path: str, module_name: str):
        self.config = {}
        self.project_path = project_path
        self.module_name = module_name
        if self.project_path[0] != '/':
            self.project_path = os.path.abspath(self.project_path)
        self.dir = project_path + '/.pyster'
        self.name = module_name + '.json'

    def __str__(self):
        return str(self.config)

    def read_from_config(self):
        if not os.path.exists(os.path.join(self.dir, self.name)):
            raise FileNotFoundError
        with open(os.path.join(self.dir, self.name)) as json_file:
            self.config = json.load(json_file)

    def dump_to_config(self):
        if not os.path.exists(os.path.join(self.dir)):
            os.makedirs(os.path.join(self.dir))
        with open(os.path.join(self.dir, self.name), 'w') as of:
            json.dump(self.config, of)

    def add_module(self, module_info: list):
        [module_name] = module_info
        if module_name not in self.config.keys():
            self.config[module_name] = {}

    def add_class(self, class_info: list):
        [module_name, class_name] = class_info
        if class_name not in self.config[module_name].keys():
            self.config[module_name][class_name] = {"__init__": [
                {"self": ""}
            ]}

    def add_func(self, func_info: list):
        [module_name, class_name, func_name, func_sig] = func_info
        self.config[module_name][class_name][func_name] = []
        counter = 0
        for _, arg in func_sig.items():
            sub_type = 'any'

            if arg.name == 'self':
                arg_type = 'self'
            elif arg.annotation != arg.empty:
                if type(arg.annotation) == type:
                    arg_type = arg.annotation.__name__
                # handle typing.List type
                elif type(arg.annotation.__origin__) == type(
                        typing.List.__origin__):
                    arg_type = arg.annotation.__origin__.__name__
                    sub_type = arg.annotation.__args__[0].__name__
                else:
                    arg_type = 'any'
            else:
                arg_type = 'any'

            self.config[module_name][class_name][func_name].append(
                {arg_type: ""})

            if arg.default != arg.empty:
                self.add_default_val(
                    [module_name, class_name, func_name, counter,
                     arg_type], arg.default, sub_type)
            counter += 1

    def add_default_val(self, def_info, default_val, sub_type='any'):
        [module_name, class_name, func_name, arg_pos, arg_type] = def_info
        if arg_type == 'list':
            list_params = []
            for val in default_val:
                list_params.append({sub_type: val})
            default_val = list_params

        self.config[module_name][class_name][func_name][arg_pos][
            arg_type] = default_val

    def add_type_override(self, over_info):
        [module_name, class_name, func_name, arg_pos, arg_obj] = over_info
        assign_type(self.config[module_name][class_name][func_name][arg_pos],
                    arg_obj)
