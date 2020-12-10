from os import path

from pyster.init.staticParse import UserModule
from pyster.gen.covDrivenFilter import CoverageDrivenFilter
from pyster.common import ConfigObject


def test_gen_foobar_tests():
    project_path = "tests/foobar"
    module_name = "foobar.foobar"
    coverage_target = 100
    timeout = 3
    user_tests = []
    config = ConfigObject(project_path, module_name)
    UserModule(project_path, module_name, config)
    config.dump_to_config()
    config.read_from_config()
    CoverageDrivenFilter(config, coverage_target, timeout, user_tests).generate()
    assert path.exists("tests/foobar/foobarFoobarTest.py")
