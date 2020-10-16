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

    # Print all classes inside the module
    print([m[0] for m in inspect.getmembers(mod, inspect.isclass) if m[1].__module__ == module_name])
