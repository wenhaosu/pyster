import json
import os


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
                        [module_name, class_name, func_name, counter,
                         arg_type],
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
        pass
