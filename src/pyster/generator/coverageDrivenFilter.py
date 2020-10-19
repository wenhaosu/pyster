import coverage
import sys
sys.path.insert(1, '../')

class CoverageDrivenFilter(object):
    def __init__(self, module_obj: any):
        self.class_module = module_obj
    
    def test_coverage(self):
        sys.path.insert(1, self.class_module.module_path)
        user_module = __import__(self.class_module.module_name)

        cov = coverage.Coverage()
        cov.start()

        # Replace with calling the functions in the module
        user_module.main()

        # .. call your code ..

        cov.stop()
        cov.save()
        cov.report()
        cov.json_report()
        return


