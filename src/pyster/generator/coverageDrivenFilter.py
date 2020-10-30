from generator.testFileGenerator import TestFileGenerator
from generator.generateRandomInput import TestCase
import os


class CoverageDrivenFilter:

    def __init__(self, user_module: any):
        # code for getting a dict of generated tests
        self.module_item = user_module

    def generate_tests(self):
        ret_dict = {'module_name': self.module_item.module_name,
                    'classes': []}

        for c_name, c_obj in self.module_item.module_classes.items():
            class_dict = {'class_name': c_name,
                          'funcs': []}
            for f in c_obj.class_funcs:
                func_dict = {'func_name': f[0],
                             'tests': []}
                tc = TestCase(getattr(self.module_item.mod, c_name),
                              c_obj.class_init, f)
                for _ in range(2):
                    tc_dict = tc.generate_random_test()
                    func_dict['tests'].append(tc_dict)
                class_dict['funcs'].append(func_dict)
            ret_dict['classes'].append(class_dict)

            print(class_dict)

            generator = TestFileGenerator(self.module_item.module_name, c_name)
            generator.dump(class_dict)
            generator.write_to_file(os.path.join(
                self.module_item.module_path, c_name + 'Test.py'))