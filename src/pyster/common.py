import json
import os


def indent(n: int):
    return "\t" * n

primitive = (int, str, bool, float)

def is_primitive(value):
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
    def __init__(self, path: str):
        self.config = {}
        self.path = path

    def __str__(self):
        return json.dumps(self.config, indent=4)

    def read_from_config(self):
        pass

    def dump_to_config(self):
        pass

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
            arg = str(arg)
            sub_type = 'any'

            if arg == 'self':
                arg_type = 'self'
            elif ':' in arg:
                if '=' in arg:
                    arg_type = arg[arg.find(': ') + 2:arg.rfind(' =')]
                else:
                    arg_type = arg.split(': ', 1)[1]
            else:
                arg_type = 'any'

            # handle List[int] type
            if arg_type.startswith('List'):
                sub_type = arg_type[5:-1]
                arg_type = 'list'

            self.config[module_name][class_name][func_name].append(
                {arg_type: ""})

            # TODO: Use type directly instead of parsing a string
            if '=' in arg:
                if ':' in arg:
                    self.add_default_val(
                        [module_name, class_name, func_name, counter, arg_type],
                        arg[arg.find('= ') + 2:], sub_type)
                else:
                    self.add_default_val(
                        [module_name, class_name, func_name, counter,
                         arg_type],
                        arg[arg.find('=') + 1:], sub_type)
            counter += 1

    def add_default_val(self, def_info, default_val, sub_type='any'):
        [module_name, class_name, func_name, arg_pos, arg_type] = def_info
        if arg_type == 'list':
            type_vec = []
            val_vec = []
            default_val = default_val[1:-1].split(",")
            for val in default_val:
                type_vec.append(sub_type)
                if sub_type != 'any':
                    val = eval(sub_type + '(' + val + ')')
                val_vec.append(val)

            default_val = [type_vec, val_vec]

        self.config[module_name][class_name][func_name][arg_pos][
            arg_type] = default_val

    def add_type_override(self, over_info):
        [module_name, class_name, func_name, arg_pos, arg_obj] = over_info
        assign_type(self.config[module_name][class_name][func_name][arg_pos], arg_obj) 

        


        
