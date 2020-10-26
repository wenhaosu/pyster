import importlib
import inspect
import logging
import os
import sys

from generator.common import indent


class UserClass(object):
    def __init__(self, module_obj: any, class_name: str):
        self.class_module = module_obj
        self.class_name = class_name
        self.class_funcs = []
        self.class_init = None

    def __str__(self, ind=0):
        ret_str = indent(ind) + "== class name: " + self.class_name + "\n"
        for m in self.class_funcs:
            ret_str += indent(ind + 1) + "== callable name: " + m[0] + "\n"
            ret_str += indent(ind + 2) + "== signature: " + repr(
                inspect.signature(m[1])) + "\n"
        return ret_str

    def parse_class(self):
        try:
            self.class_module in sys.modules
        except ModuleNotFoundError:
            logging.exception("message")
        else:
            # Get all function objects from a class
            attrs = getattr(self.class_module, self.class_name)
            for func in inspect.getmembers(attrs, inspect.isfunction):
                if func[0] == '__init__':
                    self.class_init = func
                else:
                    self.class_funcs.append(func)


class UserModule(object):
    def __init__(self, abs_path: str):
        self.abs_path = abs_path
        self.module_path = ""
        self.module_name = ""
        self.module_classes = {}
        self.mod = None
        self.parse_module()

    def __str__(self, ind=0):
        ret_str = indent(ind) + "== module name: " + self.module_name + "\n"
        for _, v in self.module_classes.items():
            ret_str += v.__str__(1)
        return ret_str

    def parse_module(self):
        try:
            os.path.isfile(self.abs_path)
        except FileNotFoundError:
            logging.exception("message")
        else:
            # Store module path and module name
            delimiter = self.abs_path.rfind('/')
            self.module_path = self.abs_path[0:delimiter]
            self.module_name = self.abs_path[delimiter + 1:-3]

            # Import the file as module and retrieve all class names
            sys.path.insert(0, self.module_path)
            self.mod = importlib.import_module(self.module_name)
            class_temp = []
            for m in inspect.getmembers(self.mod, inspect.isclass):
                class_temp.append(m[0])

            # Fill in self.module_classes with UserClass objects
            for c in class_temp:
                self.module_classes[c] = UserClass(self.mod, c)
                self.module_classes[c].parse_class()
