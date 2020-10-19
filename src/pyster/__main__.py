import sys
import argparse
from generator.getClassInfo import UserModule
from generator.coverageDrivenFilter import CoverageDrivenFilter

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Unit Tests')
    parser.add_argument('Path',
                       metavar='path',
                       type=str,
                       help='the path to source files')
    parser.add_argument('Timeout',
                       metavar='timeout',
                       type=int,
                       help='user defined time limit for the program to run in seconds')
    parser.add_argument('Coverage_target',
                       metavar='coverage_target',
                       type=int,
                       help='Target coverage for the generated tests in percentage')
    args = parser.parse_args()
    file_path = args.Path
    module_item = UserModule(file_path)
    test_filter = CoverageDrivenFilter(module_item)
    print(module_item)
    test_filter.test_coverage()
