import os

from coverage import coverage
from coverage.jsonreport import JsonReporter

from .testRunner import UnitTest
from ..common import ConfigObject, indent
from .genRandomArg import FuncTest
from .testFileGenerator import TestFileGenerator


class CoverageDrivenFilter:

    def __init__(self, config: ConfigObject, coverage: int):
        # code for getting a dict of generated tests
        self.config = config
    
    def generate(self):
        config = self.config
        config.read_from_config()
        test_list = []
        test_list_exception = []
        cov = coverage()
        cov.start()
        for module_name, temp in config.config.items():
            if module_name == config.module_name:
                for class_name, val in temp.items():
                    for func_name, _ in val.items():
                        func = FuncTest(config,
                                        [module_name, class_name, func_name])
                        print('----------')
                        test_info = func.generate_random_test()
                        print(test_info)
                        test = UnitTest(test_info, config)
                        try:
                            test.run()
                            test_list.append(test)
                        except Exception as e:
                            print(type(e).__name__)
                            test.exception = e
                            print("Exception found in {}: ".format(func_name) + str(e))
                            test_list_exception.append(test)
                        test.dump()
                        for i in test.output:
                            print(i)
                        print()
        cov.stop()

        json_rep = JsonReporter(cov)
        cov_json_file = os.path.join(config.project_path, ".pyster", "coverage_temp.json")
        with open(cov_json_file, 'w') as f:
            json_rep.report(morfs=[config.get_file_path()], outfile=f)

        
        generator = TestFileGenerator(config, test_list + test_list_exception)
        generator.dump()
        module_camal_name = "".join([i.capitalize() for i in config.module_name.split('.')])
        generator.write_to_file(os.path.join(config.project_path, module_camal_name[0].lower() + module_camal_name[1:] + "Test.py"))
                        
