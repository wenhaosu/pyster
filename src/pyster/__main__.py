import argparse
import logging
# from generator.getClassInfo import UserModule
# from generator.generateRandomInput import TestCase
# from generator.testFileGenerator import TestFileGenerator
# from generator.coverageDrivenFilter import CoverageDrivenFilter

from .init.staticParse import UserModule
from .common import ConfigObject

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Unit Tests')
    parser.add_argument('path',
                        metavar='path',
                        type=str,
                        help='the path to source files')
    parser.add_argument('--timeout',
                        metavar='timeout',
                        type=int,
                        default=20,
                        help='user defined time limit for the program to run in seconds')
    parser.add_argument('--coverage',
                        metavar='coverage_target',
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
        # module_item = UserModule(file_path, config)
        # print(module_item)
        # print(config)
        # print(config.dir)
        config.read_from_config()
        print(config)

        # coverageFilter = CoverageDrivenFilter(module_item)
        # coverageFilter.generate_tests()

    except Exception as e:
        logging.exception(e)
