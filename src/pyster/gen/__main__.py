import argparse
import logging

from ..common import ConfigObject
from .genRandomArg import FuncTest

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Unit Tests')
    parser.add_argument('path',
                        metavar='path',
                        type=str,
                        help='the path to source files')
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
        config.read_from_config()
        for module_name, temp in config.config.items():
            if module_name == 'foobar.foobar':
                for class_name, val in temp.items():
                    for func_name, _ in val.items():
                        func = FuncTest(config, [module_name, class_name, func_name])
                        print('----------')
                        print(func_name)
                        print(func.generate_random_test())


    except Exception as e:
        logging.exception(e)
