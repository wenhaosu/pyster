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
    coverage_target = args.coverage

    notify("project_path: " + project_path, Colors.ColorCode.cyan)
    notify("module_name: " + module_name, Colors.ColorCode.cyan)
    notify("timeout: " + str(timeout), Colors.ColorCode.cyan)
    notify("coverage_target: " + str(coverage_target), Colors.ColorCode.cyan)

    if project_path == '' or module_name == '':
        print("Please enter a valid project path / module name.")
        exit(-1)

    config = ConfigObject(project_path, module_name)

    try:
        filter = CoverageDrivenFilter(config, coverage_target)
        filter.generate()
    except Exception as e:
        logging.exception(e)
