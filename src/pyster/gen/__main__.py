import argparse
import logging
import os
from pprint import PrettyPrinter
from coverage import coverage

from coverage.jsonreport import JsonReporter

from ..common import ConfigObject, Colors, notify
from .genRandomArg import FuncTest
from .testFileGenerator import TestFileGenerator
from .covDrivenFilter import CoverageDrivenFilter
from .testRunner import UnitTest

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
    parser.add_argument('--user_tests',
                        metavar='user_tests',
                        nargs='*',
                        default='',
                        help='user tests to run before measuring coverage')
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
    user_tests = args.user_tests
    timeout = args.timeout
    coverage_target = args.coverage

    notify("project_path: " + project_path, Colors.ColorCode.cyan)
    notify("module_name: " + module_name, Colors.ColorCode.cyan)
    notify("user_tests: " + str(user_tests), Colors.ColorCode.cyan)
    notify("timeout: " + str(timeout), Colors.ColorCode.cyan)
    notify("coverage_target: " + str(coverage_target), Colors.ColorCode.cyan)

    if project_path == '' or module_name == '':
        # TODO: report error if path or module is wrong
        print("Please enter a valid project path / module name.")
        exit(-1)

    config = ConfigObject(project_path, module_name)
    config.read_from_config()

    try:
        cov_filter = CoverageDrivenFilter(config, coverage_target, timeout,
                                          user_tests)
        cov_filter.generate()
    except Exception as e:
        logging.exception(e)
