import json
import os
import typing
import sys
import argparse


def indent(n: int):
    return "\t" * n


class Colors:
    reset = "\033[0m"

    class ColorCode:
        red = "\033[31m"
        green = "\033[32m"
        orange = "\033[33m"
        yellow = "\033[93m"
        cyan = "\033[36m"
        lightcyan = "\033[96m"


def notify(msg, color=Colors.reset):
    sys.stderr.write(color + "== " + msg + "\n" + Colors.reset)
    sys.stderr.flush()


def notify_init_params(args, stage="init"):
    project_path = args.project_path
    module_name = args.module_name
    notify("project_path: " + project_path, Colors.ColorCode.cyan)
    notify("module_name: " + module_name, Colors.ColorCode.cyan)
    if stage != "init":
        notify("user_tests: " + str(args.user_tests), Colors.ColorCode.cyan)
        notify("timeout: " + str(args.timeout), Colors.ColorCode.cyan)
        notify("coverage_target: " + str(args.coverage), Colors.ColorCode.cyan)


primitive = [int, str, bool, float]
primitive_str = ["int", "str", "bool", "float"]

parser = argparse.ArgumentParser(description="Generate Pyster Config File")
parser.add_argument(
    "--project_path",
    metavar="project_path",
    default="",
    type=str,
    help="the path to Python project",
)
parser.add_argument(
    "--module_name",
    metavar="module_name",
    default="",
    type=str,
    help="the module for test generation",
)
parser.add_argument(
    "-r",
    "--path_runtime",
    metavar="path_runtime",
    type=str,
    default="",
    help="the path to code to exercise the tool",
    required=False,
)
parser.add_argument(
    "--user_tests",
    metavar="user_tests",
    nargs="*",
    default="",
    help="user tests to run before measuring coverage",
)
parser.add_argument(
    "-t",
    "--timeout",
    metavar="timeout",
    type=int,
    default=20,
    help="user defined time limit for the program to run in seconds",
)
parser.add_argument(
    "-c",
    "--coverage",
    metavar="target",
    type=int,
    default=80,
    choices=range(1, 101),
    help="target coverage for the generated tests in percentage",
)


def is_primitive(value):
    if type(value) == str:
        if value in primitive_str:
            return True
    return value in primitive


def check_path_valid(project_path: str, module_name: str):
    if project_path == "" or module_name == "":
        # TODO: report error if path or module is wrong
        print("Please enter a valid project path / module name.")
        exit(-1)


def assign_type(config_dict, value):
    config_dict.pop("any", None)
    if isinstance(value, dict):
        config_dict["dict"] = value
    elif isinstance(value, list):
        config_dict["list"] = []
        for item in value:
            config_dict["list"].append(dict())
            assign_type(config_dict["list"][-1], item)
    elif is_primitive(value):
        config_dict[type(value).__name__] = value
    else:
        config_dict[type(value).__name__] = ""


class ConfigObject(object):
    def __init__(self, project_path: str, module_name: str):
        self.config = {}
        self.project_path = project_path
        self.module_name = module_name
        # if self.project_path[0] != '/':
        #     self.project_path = os.path.abspath(self.project_path)
        self.dir = project_path + "/.pyster"
        self.name = module_name + ".json"

    def __str__(self):
        return str(self.config)

    def get_file_path(self):
        module_file = self.module_name.split(".")
        module_file[-1] += ".py"
        return os.path.join(self.project_path, *module_file)

    def read_from_config(self):
        if not os.path.exists(os.path.join(self.dir, self.name)):
            raise FileNotFoundError
        with open(os.path.join(self.dir, self.name)) as json_file:
            self.config = json.load(json_file)

    def dump_to_config(self):
        if not os.path.exists(os.path.join(self.dir)):
            os.makedirs(os.path.join(self.dir))
        with open(os.path.join(self.dir, self.name), "w") as of:
            json.dump(self.config, of)
        notify("Finish parsing: " + self.module_name + "!", Colors.ColorCode.green)
        num_funcs = 0
        for _, val in self.config[self.module_name].items():
            num_funcs += len(val)
        notify(
            "Totally parsed: "
            + str(len(self.config[self.module_name]))
            + " modules, "
            + str(num_funcs)
            + " functions",
            Colors.ColorCode.green,
        )

    def add_module(self, module_info: list):
        [module_name] = module_info
        if module_name not in self.config.keys():
            self.config[module_name] = {}

    def add_class(self, class_info: list, add_init: bool = True):
        [module_name, class_name] = class_info
        if class_name not in self.config[module_name].keys():
            self.config[module_name][class_name] = (
                {"__init__": [{"self": ""}]} if add_init else {}
            )

    def add_func(self, func_info: list):
        [module_name, class_name, func_name, func_sig] = func_info
        self.config[module_name][class_name][func_name] = []
        counter = 0
        for _, arg in func_sig.items():
            sub_type = "any"

            if arg.name == "self":
                arg_type = "self"
            elif arg.annotation != arg.empty:
                if type(arg.annotation) == type:
                    arg_type = arg.annotation.__name__
                # handle typing.List type
                elif not hasattr(arg.annotation, "__origin__"):
                    arg_type = "any"
                elif type(arg.annotation.__origin__) == type(typing.List.__origin__):
                    arg_type = arg.annotation.__origin__.__name__
                    sub_type = (
                        arg.annotation.__args__[0].__name__
                        if is_primitive(arg.annotation.__args__[0])
                        else None
                    )
                else:
                    arg_type = "any"
            else:
                arg_type = "any"

            self.config[module_name][class_name][func_name].append({arg_type: ""})

            if (
                arg.default != arg.empty
                and arg.default != None
                and (
                    is_primitive(type(arg.default))
                    or (
                        arg.annotation != arg.empty
                        and type(arg.annotation) != type
                        and hasattr(arg.annotation, "__origin__")
                        and type(arg.annotation.__origin__)
                        == type(typing.List.__origin__)
                    )
                )
            ):
                self.add_default_val(
                    [module_name, class_name, func_name, counter, arg_type],
                    arg.default,
                    sub_type,
                )
            counter += 1

    def add_default_val(self, def_info, default_val, sub_type="any"):
        [module_name, class_name, func_name, arg_pos, arg_type] = def_info
        if arg_type == "list":
            list_params = []
            for val in default_val:
                list_params.append({sub_type: val})
            default_val = list_params

        self.config[module_name][class_name][func_name][arg_pos][arg_type] = default_val

    def add_type_override(self, over_info):
        [module_name, class_name, func_name, arg_pos, arg_obj] = over_info
        if module_name not in self.config:
            return
        if class_name not in self.config[module_name]:
            return
        if func_name not in self.config[module_name][class_name]:
            return
        assign_type(self.config[module_name][class_name][func_name][arg_pos], arg_obj)
