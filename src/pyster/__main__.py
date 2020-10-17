import importlib
import inspect
import sys

if __name__ == "__main__":
    # Get user input of target file
    file_path = sys.argv[1] # TODO: Use argparse library for formatted input

    # Retrive file path and import the file as module
    delimiter = file_path.rfind('/')
    module_path, module_name = file_path[0:delimiter], file_path[delimiter+1:-3]

    sys.path.insert(0, module_path)
    mod = importlib.import_module(module_name)

    # Print all classes inside a module / all funcs inside a class
    mod_classes = []
    class_funcs = {}

    for m in inspect.getmembers(mod, inspect.isclass):
        mod_classes.append(m[0])

    for c in mod_classes:
        class_funcs[c] = (inspect.getmembers(getattr(mod, c), inspect.isfunction))

    print(mod_classes)
    print(class_funcs)
