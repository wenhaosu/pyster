import argparse
import logging
# from generator.getClassInfo import UserModule
# from generator.generateRandomInput import TestCase
# from generator.testFileGenerator import TestFileGenerator
# from generator.coverageDrivenFilter import CoverageDrivenFilter

from .init.staticParse import UserModule
from .init.runtimeParse import RuntimeParser
from .common import ConfigObject

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Unit Tests')
    parser.add_argument('path',
                        metavar='path',
                        type=str,
                        help='the path to source files')
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
    file_path = args.path
    print("timeout: " + str(args.timeout))
    print("coverage_target: " + str(args.coverage))

    config = ConfigObject(file_path)

    try:
        module_item = UserModule(file_path, config)
        parser = RuntimeParser(module_item.module_name, config, args.path_runtime)
        parser.parse()
        config.dump_to_config()

        print(config)

        # coverageFilter = CoverageDrivenFilter(module_item)
        # coverageFilter.generate_tests()

    except Exception as e:
        logging.exception(e)
