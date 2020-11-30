import argparse
import logging

from .staticParse import UserModule
from .runtimeParse import RuntimeParser
from ..common import ConfigObject, Colors, notify

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Unit Tests')
    parser.add_argument('--project_path',
                        metavar='project_path',
                        default='',
                        type=str,
                        help='the path to Python project')
    parser.add_argument('--module_name',
                        metavar='module_name',
                        default='',
                        type=str,
                        help='the module for test generation')
    parser.add_argument('-r', '--path_runtime',
                        metavar='path_runtime',
                        type=str,
                        default="",
                        help='the path to code to exercise the tool')
    args = parser.parse_args()
    project_path = args.project_path
    module_name = args.module_name

    notify("project_path: " + project_path, Colors.ColorCode.cyan)
    notify("module_name: " + module_name, Colors.ColorCode.cyan)

    if project_path == '' or module_name == '':
        print("Please enter a valid project path / module name.")
        exit(-1)

    config = ConfigObject(project_path, module_name)

    try:
        module_item = UserModule(project_path, module_name, config)
        parser = RuntimeParser(config.module_name, config, args.path_runtime)
        parser.parse()
        config.dump_to_config()

        print(config)

    except Exception as e:
        logging.exception(e)
