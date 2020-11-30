import argparse
import logging
# from generator.getClassInfo import UserModule
# from generator.generateRandomInput import TestCase
# from generator.testFileGenerator import TestFileGenerator
# from generator.coverageDrivenFilter import CoverageDrivenFilter

from .init.staticParse import UserModule
from .init.runtimeParse import RuntimeParser
from .common import ConfigObject, Colors, notify

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
    parser.add_argument('-t', '--timeout',
                        metavar='timeout',
                        type=int,
                        default=20,
                        help='user defined time limit for the program to run in seconds')
    parser.add_argument('-c', '--coverage',
                        metavar='target',
                        type=int,
                        default=80,
                        choices=range(1, 101),
                        help='target coverage for the generated tests in percentage')
    args = parser.parse_args()
    project_path = args.project_path
    module_name = args.module_name
    timeout = args.timeout
    coverage = args.coverage

    notify("project_path: " + project_path, Colors.ColorCode.cyan)
    notify("module_name: " + module_name, Colors.ColorCode.cyan)
    notify("timeout: " + str(timeout), Colors.ColorCode.cyan)
    notify("coverage_target: " + str(coverage), Colors.ColorCode.cyan)

    if project_path == '' or module_name == '':
        print("Please enter a valid project path / module name.")
        exit(-1)

    print("timeout: " + str(timeout))
    print("coverage_target: " + str(coverage))

    config = ConfigObject(project_path, module_name)

    try:
        module_item = UserModule(project_path, module_name, config)
        parser = RuntimeParser(config.module_name, config, args.path_runtime)
        parser.parse()
        config.dump_to_config()

        print(config)

        # coverageFilter = CoverageDrivenFilter(module_item)
        # coverageFilter.generate_tests()

    except Exception as e:
        logging.exception(e)
