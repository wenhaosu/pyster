import json
import os
import typing
from typing_inspect import get_origin


def indent(n: int):
    return "\t" * n


class ConfigObject(object):
    def __init__(self, path: str):
        self.config = {}
        self.path = path
        if self.path[0] != '/':
            self.path = os.path.abspath(self.path)
        self.dir = self.path.rsplit('/', 1)[0] + '/.pyster'
        self.name = self.path.rsplit('/', 1)[1][:-3] + '.json'

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
        self.config[module_name] = {}

    def add_class(self, class_info: list):
        [module_name, class_name] = class_info
        self.config[module_name][class_name] = {}

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
                elif type(arg.annotation) == type(typing.List):
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
        pass
