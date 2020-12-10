from os import path

from pyster.init.staticParse import UserModule
from pyster.init.runtimeParse import RuntimeParser
from pyster.common import ConfigObject


def test_static_parse_foobar():
    project_path = "tests/foobar"
    module_name = "foobar.foobar"
    config = ConfigObject(project_path, module_name)
    UserModule(project_path, module_name, config)
    config.dump_to_config()
    assert path.exists("tests/foobar/.pyster/foobar.foobar.json")


def test_runtime_parse_foobar():
    project_path = "tests/foobar"
    module_name = "foobar.foobar"
    path_runtime = "tests/foobar/foobarRuntime.py"
    config = ConfigObject(project_path, module_name)
    UserModule(project_path, module_name, config)
    parser = RuntimeParser(config.module_name, config, path_runtime)
    parser.parse()
    config.dump_to_config()
    assert path.exists("tests/foobar/.pyster/foobar.foobar.json")
