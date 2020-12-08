import os
import time
import random
import sys

from coverage import coverage
from coverage.jsonreport import JsonReporter

from .testRunner import UnitTest
from ..common import ConfigObject, notify, Colors
from .genRandomArg import FuncTest
from .testFileGenerator import TestFileGenerator


class CoverageDrivenFilter:
    def __init__(
        self, config: ConfigObject, _coverage: int, _timeout: int, _user_tests: list
    ):
        self.config = config
        self.coverage_target = _coverage
        self.timeout = _timeout
        self.user_tests = _user_tests
        self.coverage_init = 0
        self.coverage_val = 0
        self.cov_json_file = os.path.join(
            self.config.project_path, ".pyster", "coverage_temp.json"
        )

    def init_user_test_run(self):
        notify("Running user test suite...", Colors.ColorCode.orange)
        files = " ".join(f for f in self.user_tests)
        os.system("coverage run -m pytest " + files)

    def dump_cov_info(self, cov, first_trial=False):
        json_rep = JsonReporter(cov)
        with open(self.cov_json_file, "w") as f:
            json_rep.report(morfs=[self.config.get_file_path()], outfile=f)
        cov_rate_before = self.coverage_val
        self.coverage_val = json_rep.report_data["totals"]["percent_covered"]
        if first_trial:
            self.coverage_init = self.coverage_val
        return self.coverage_val > cov_rate_before

    def notify_test_found(self, test_info):
        func_name = (
            str(test_info["class_name"]) + "." + str(test_info["func_name"])
            if test_info["class_name"] != ""
            else str(test_info["func_name"])
        )
        notify("Test found for function: " + func_name)
        notify("Current coverage: " + str(self.coverage_val))

    def generate(self):
        config = self.config
        cov = coverage(auto_data=True, data_file=".coverage")
        if len(self.user_tests) != 0:
            self.init_user_test_run()
            cov.load()
        self.dump_cov_info(cov, True)

        test_list, test_list_exception = self.generate_with_time_limit(cov)

        generator = TestFileGenerator(config, test_list + test_list_exception)
        generator.dump()
        module_camel_name = "".join(
            [i.capitalize() for i in config.module_name.split(".")]
        )
        generator.write_to_file(
            os.path.join(
                config.project_path,
                module_camel_name[0].lower() + module_camel_name[1:] + "Test.py",
            )
        )
        notify(
            "Coverage before running: " + str(self.coverage_init),
            Colors.ColorCode.orange,
        )
        notify(
            "Coverage after running: " + str(self.coverage_val), Colors.ColorCode.green
        )

    def generate_with_time_limit(self, cov):
        config = self.config
        test_list = []
        test_list_exception = []

        time_begin = time.time()
        # 1. Run all functions once in the first Trial
        for class_name, class_val in config.config[config.module_name].items():
            for func_name, _ in class_val.items():
                if (
                    self.coverage_val >= self.coverage_target
                    or time.time() - time_begin > self.timeout
                ):
                    return test_list, test_list_exception
                self.generate_for_func(
                    test_list,
                    test_list_exception,
                    config.module_name,
                    class_name,
                    func_name,
                    cov,
                )

        # 2. Randomly select a function and run a trial
        while time.time() - time_begin < self.timeout:
            if self.coverage_val >= self.coverage_target:
                break
            class_name, class_val = random.choice(
                list(config.config[config.module_name].items())
            )
            if len(class_val.items()) == 0:
                continue
            func_name, _ = random.choice(list(class_val.items()))
            self.generate_for_func(
                test_list,
                test_list_exception,
                config.module_name,
                class_name,
                func_name,
                cov,
            )

        return test_list, test_list_exception

    def generate_for_func(
        self, test_list, test_list_exception, module_name, class_name, func_name, cov
    ):
        func = FuncTest(self.config, [module_name, class_name, func_name])
        cov.start()
        test_info = func.generate_random_test()
        test = UnitTest(test_info, self.config)
        try:
            # Redirect all intermediate print to devnull
            normal_out = sys.stdout
            null_out = open(os.devnull, "w")
            sys.stdout = null_out
            test.run()
            sys.stdout = normal_out
            cov.stop()
            if self.dump_cov_info(cov):
                self.notify_test_found(test_info)
                test_list.append(test)
                test.dump()
        except Exception as e:
            test.exception = e
            cov.stop()
            if self.dump_cov_info(cov):
                self.notify_test_found(test_info)
                test_list_exception.append(test)
                test.dump()
