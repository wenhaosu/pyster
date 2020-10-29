from generator.getClassInfo import UserModule
from generator.common import indent


def gen_str(value):
    if isinstance(value, str):
        return "'" + value + "'"
    return str(value)


class TestFileGenerator:
    def __init__(self, module_name, class_name):
        self.output = []
        self.imports = [('unittest',), (class_name, module_name)]

    def gen_call(self, args, function_name, instance_name):
        call_code = instance_name + '.' + function_name + '('
        call_code += ','.join([gen_str(arg) for arg in args])
        call_code += ')'
        return call_code

    def dump_init(self, class_name):
        self.output.append(
            indent(2) + class_name.lower() + ' = ' + class_name + '()')

    def dump_assert(self, test, function_name, instance_name):
        call_code = self.gen_call(test['args'], function_name, instance_name)
        self.output.append(
            indent(2) + 'self.assertEqual({}, {})'.format(call_code, gen_str(
                test['ret'])))

    def dump_function(self, function_info, class_name):
        self.output.append(indent(1) + 'def test_{}(self):'.format(
            function_info['func_name']))
        self.dump_init(class_name)
        for test in function_info['tests']:
            self.dump_assert(test, function_info['func_name'],
                             class_name.lower())

    def dump_class(self, class_info):
        self.output.append('class {}(unittest.TestCase):'.format(
            class_info['class_name'] + 'Test'))
        for func in class_info['funcs']:
            self.dump_function(func, class_info['class_name'])
            self.output.append('')
        self.output.append('')

    def dump_main(self):
        self.output.append('if __name__ == "__main__":')
        self.output.append(indent(1) + 'unittest.main()')

    def dump_imports(self):
        for imp in self.imports:
            if len(imp) == 1:
                self.output.append('import ' + imp[0])
            if len(imp) == 2:
                self.output.append('from ' + imp[1] + ' import ' + imp[0])
        self.output.append('')
        self.output.append('')

    def dump(self, class_info):
        self.output = []
        self.dump_imports()
        self.dump_class(class_info)
        self.dump_main()

    def write_to_file(self, file_path):
        with open(file_path, 'w') as fp:
            for line in self.output:
                fp.write(line + '\n')
