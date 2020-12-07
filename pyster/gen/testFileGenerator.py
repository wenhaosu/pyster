from .testRunner import UnitTest
from ..common import ConfigObject


class TestFileGenerator:
    def __init__(self, config: ConfigObject, unittest_list: list):
        self.output = []
        self.module_name = config.module_name
        self.project_path = config.project_path
        self.imports = list(config.config.keys())
        self.unittests = unittest_list

    def dump_function(self, unittest: UnitTest):
        if unittest.valid:
            self.output.append(
                'def test_{}_{}():'.format(unittest.func_name.strip('_'),
                                           unittest.class_name))
            self.output += unittest.output
            self.output.append('')
            self.output.append('')

    def dump_imports(self):
        for imp in self.imports:
            self.output.append('import ' + imp)
        self.output.append('')
        self.output.append('')

    def dump(self):
        self.output = []
        self.dump_imports()
        for unittest in self.unittests:
            self.dump_function(unittest)

    def write_to_file(self, file_path):
        with open(file_path, 'w') as fp:
            for line in self.output:
                fp.write(line + '\n')
