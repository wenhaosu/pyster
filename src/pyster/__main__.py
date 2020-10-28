import argparse
import logging
from generator.getClassInfo import UserModule
from generator.generateRandomInput import TestCase
from generator.testFileGenerator import TestFileGenerator

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

    try:
        module_item = UserModule(file_path)
        print(module_item)

        # code for getting a dict of generated tests
        ret_dict = {'module_name': module_item.module_name,
                    'classes': []}

        generater = TestFileGenerator()

        for c_name, c_obj in module_item.module_classes.items():
            class_dict = {'class_name': c_name,
                          'funcs': []}
            for f in c_obj.class_funcs:
                func_dict = {'func_name': f[0],
                             'tests': []}
                tc = TestCase(getattr(module_item.mod, c_name), f)
                for i in range(5):
                    tc_dict = tc.generate_random_test()
                    func_dict['tests'].append(tc_dict)
                class_dict['funcs'].append(func_dict)
            ret_dict['classes'].append(class_dict)

        print (class_dict)
        generater.dump(class_dict)
        generater.write_to_file(module_item.module_path +  '/' + c_name + 'Test.py')

        #print(ret_dict)
    except Exception as e:
        logging.exception(e)
