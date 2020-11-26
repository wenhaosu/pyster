import importlib
import inspect
import logging
import os
import sys

from ..common import indent, ConfigObject

module_to_parse = ""


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
            ret_str += indent(ind + 2) + "== signature: " + repr(
                inspect.signature(m[1])) + "\n"
        return ret_str

    def parse_class(self, config: ConfigObject):
        # Get all function objects from a class
        global module_to_parse
        attrs = getattr(self.class_module, self.class_name)
        for func in inspect.getmembers(attrs, inspect.isfunction):
            if func[0] == '__init__' or module_to_parse == self.module_name:
                self.class_funcs.append(func)
                config.add_func(
                    [self.class_module.__name__, self.class_name, func[0],
                     inspect.signature(func[1]).parameters])


class UserModule(object):
    def __init__(self, abs_path: str, config: ConfigObject):
        self.abs_path = abs_path
        self.module_path = ""
        self.module_name = ""
        self.module_classes = {}
        self.mod = None
        self.parse_module(config)

    def __str__(self, ind: int = 0):
        ret_str = indent(ind) + "== module name: " + self.module_name + "\n"
        for _, v in self.module_classes.items():
            ret_str += v.__str__(1)
        return ret_str

    def parse_module(self, config: ConfigObject):
        global module_to_parse
        try:
            os.path.isfile(self.abs_path)
        except FileNotFoundError:
            logging.exception("message")
        else:
            # Store module path and module name
            deli = self.abs_path.rfind('/', 0, self.abs_path.rfind('/'))
            self.module_path = self.abs_path[0:deli]
            self.module_name = self.abs_path[deli + 1:].replace('/', '.')[:-3]

            # Import the file as module and retrieve all class names
            sys.path.insert(0, self.module_path)
            if module_to_parse == "":
                module_to_parse = self.module_name
            self.mod = importlib.import_module(self.module_name)

            config.add_module([self.module_name])
            class_temp = []
            for m in inspect.getmembers(self.mod, inspect.isclass):
                curr_mod = m[1].__module__
                if curr_mod == self.module_name:
                    class_temp.append(m[0])
                else:
                    # Recursively add initializer for third party modules
                    config.add_module([curr_mod])
                    new_module_path = os.path.join(self.module_path,
                                                   curr_mod.replace('.', '/')
                                                   + '.py')
                    UserModule(new_module_path, config)

            # Fill in self.module_classes with UserClass objects
            for c in class_temp:
                self.module_classes[c] = UserClass(self.module_name, c)
                config.add_class([self.module_name, c])
                self.module_classes[c].parse_class(config)
