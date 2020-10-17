import sys
from generator.getClassInfo import UserModule

if __name__ == '__main__':
    file_path = sys.argv[1] # TODO: Use argparse library for formatted input
    module_item = UserModule(file_path)
    print(module_item)
