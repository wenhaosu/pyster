# Pyster

Pyster is a coverage-driven automatic unit test generator for Python projects.

## Pre-request
- Python 3
- [Coverage.py](https://coverage.readthedocs.io/en/coverage-5.3/) (`pip3 install coverage`)
- [pytest](https://docs.pytest.org/en/stable/) (`pip3 install pytest`)

## Usage
```bash
# Stage 1: Init pyster config file
python3 -m src.pyster.init \
  --project_path <path-to-project> \
  --module_name <module-for-testing>
# Stage 2: Generate unit tests
python3 -m src.pyster.gen \
  --project_path <path-to-project> \
  --module_name <module-for-testing> \
  --timeout <timeout-limit> \
  --coverage <coverage-target>
```

```bash
# Stage 1: Init pyster config file
usage: __main__.py [-h] [--project_path project_path]
                   [--module_name module_name] [-r path_runtime]

Generate Pyster Config File

optional arguments:
  -h, --help            show this help message and exit
  --project_path project_path
                        the path to Python project
  --module_name module_name
                        the module for test generation
  -r path_runtime, --path_runtime path_runtime
                        the path to code to exercise the tool

# Stage 2: Generate unit tests
usage: __main__.py [-h] [--project_path project_path]
                   [--module_name module_name] [-t timeout] [-c target]  

Generate Unit Tests

optional arguments:
  -h, --help            show this help message and exit
  --project_path project_path
                        the path to Python project
  --module_name module_name
                        the module for test generation
  -t timeout, --timeout timeout
                        user defined time limit for the program to run in
                        seconds
  -c target, --coverage target
                        target coverage for the generated tests in percentage
```

## Test on existing samples
```bash
git submodule update --init --recursive
cd samples
./applyPatch.sh
```

## Sample execution
```bash
# Phase 1
python3 -m src.pyster.init --project_path samples/foobar --module_name foobar.foobar
# Phase 2
python3 -m src.pyster.gen --project_path samples/foobar --module_name foobar.foobar
```


## Concept
* Use built-in Python functions to obtain all methods in a Python class.
* According to the methods input, randomly generate an object instance and function arguments, with special inputs (`0`, `-1` for integers, `[]` for lists and `None` for objects also into consideration). Use `coverage.py` third-party library to get the coverage rate increment after calling the randomly generated function call.
* Repeat step 2 until we reached 100% coverage rate or the target coverage rate from user input, or the specified timeout is reached.
* Dump all auto-generated unit tests into a test file and save it into the project test suite directory, together with a before/after coverage rate of the class.
