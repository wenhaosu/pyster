import importlib
import inspect
import sys
import copy

from ..common import indent, ConfigObject, notify, Colors


class UserClass(object):
    def __init__(self, module_name: any, class_name: str):
        self.module_name = module_name
        self.class_module = importlib.import_module(module_name)
        self.class_name = class_name
        self.class_funcs = []

    def __str__(self, ind: int = 0):
        ret_str = indent(ind) + "== class name: " + self.class_name + "\n"
        for m in self.class_funcs:
            if m is None:
                return ret_str
            ret_str += indent(ind + 1) + "== callable name: " + m[0] + "\n"
            ret_str += (
                indent(ind + 2)
                + "== signature: "
                + repr(inspect.signature(m[1]))
                + "\n"
            )
        return ret_str

    def parse_class(self, config: ConfigObject):
        # Get all function objects from a class
        attrs = getattr(self.class_module, self.class_name)
        for func in inspect.getmembers(attrs, inspect.isfunction):
            if func[0] == "__init__" or config.module_name == self.module_name:
                self.class_funcs.append(func)
                config.add_func(
                    [
                        self.class_module.__name__,
                        self.class_name,
                        func[0],
                        inspect.signature(func[1]).parameters,
                    ]
                )


class UserModule(object):
    def __init__(self, project_path: str, module_name: str, config: ConfigObject):
        self.project_path = project_path
        self.module_name = module_name
        self.module_classes = {}
        self.mod = None
        if len(config.config) != 0:
            notify(
                "Statically parsing module: " + module_name + "...",
                Colors.ColorCode.yellow,
            )
        self.parse_module(config)
        print("Finish parsing " + module_name)
        if module_name == config.module_name and "" not in config.config[module_name]:
            self.parse_func(config)

    def __str__(self, ind: int = 0):
        ret_str = indent(ind) + "== module name: " + self.module_name + "\n"
        for _, v in self.module_classes.items():
            ret_str += v.__str__(1)
        return ret_str

    def parse_module(self, config: ConfigObject):
        mod_before = []
        mod_after = []

        # Import all related files as module for only once
        first_iter = False
        if self.module_name == config.module_name:
            first_iter = True
            temp_mod = list(sys.modules.keys())
            mod_before = copy.deepcopy(temp_mod)
            sys.path.insert(0, self.project_path)

        self.mod = importlib.import_module(self.module_name)
        if first_iter:
            temp_mod = list(sys.modules.keys())
            mod_after = copy.deepcopy(temp_mod)

        config.add_module([self.module_name])

        # Recursively add initializer for third party modules
        if first_iter:
            for m in mod_after:
                if m not in mod_before:
                    config.add_module([m])
                    UserModule(self.project_path, m, config)

        # Fill in self.module_classes with UserClass objects
        class_temp = []
        for m in inspect.getmembers(self.mod, inspect.isclass):
            if m[1].__module__ == self.module_name:
                class_temp.append(m[0])

        for c in class_temp:
            self.module_classes[c] = UserClass(self.module_name, c)
            config.add_class([self.module_name, c])
            self.module_classes[c].parse_class(config)

    def parse_func(self, config):
        config.add_class([self.module_name, ""], False)
        for m in inspect.getmembers(self.mod, inspect.isfunction):
            if m[1].__module__ == self.module_name:
                config.add_func(
                    [
                        self.module_name,
                        "",
                        m[0],
                        inspect.signature(m[1]).parameters,
                    ]
                )
