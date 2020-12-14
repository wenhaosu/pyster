# Pyster
[![Build Status](https://travis-ci.com/WenhaoSu/pyster.svg?branch=main)](https://travis-ci.com/WenhaoSu/pyster) [![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Coverage Status](https://coveralls.io/repos/github/WenhaoSu/pyster/badge.svg?branch=main)](https://coveralls.io/github/WenhaoSu/pyster?branch=main) [![PyPI version](https://badge.fury.io/py/pyster-python.svg)](https://badge.fury.io/py/pyster-python)

Pyster is a coverage-driven automatic unit test generator for Python projects.

## Pre-request
- Python 3
- [Coverage.py](https://coverage.readthedocs.io/en/coverage-5.3/) (`pip3 install coverage`)
- [pytest](https://docs.pytest.org/en/stable/) (`pip3 install pytest`)

## Usage
```bash
# Stage 1: Init pyster config file
python3 -m pyster.init \
  --project_path <path-to-project> \
  --module_name <module-for-testing> \
  --path_runtime <runtime-analysis-code>
# Stage 2: Generate unit tests
python3 -m pyster.gen \
  --project_path <path-to-project> \
  --module_name <module-for-testing> \
  --user_tests <list-of-existing-test-files> \
  --timeout <timeout-limit> \
  --coverage <coverage-target>

# Run Stage 1 and Stage 2 together:
python3 -m pyster \
  --project_path <path-to-project> \
  --module_name <module-for-testing> \
  --path_runtime <runtime-analysis-code> \
  --user_tests <list-of-existing-test-files> \
  --timeout <timeout-limit> \
  --coverage <coverage-target>
```

## Test
```bash
pytest tests
```

## Sample execution
```bash
# Phase 1
python3 -m pyster.init --project_path tests/foobar --module_name foobar.foobar
# Phase 2
python3 -m pyster.gen --project_path tests/foobar --module_name foobar.foobar -t 1 -c 80
```

## Pyster Logic

![pyster-logic](https://i.imgur.com/dSWnWbF.png)

The graph above is a high-level summary of Pyster's workflow. 

Pyster contains two phases:
- **Phase 1:** Type Analysis (`init` stage)
    - Input:
        - `project_path`: Absolute/relative path to project folder
        - `module_name`: Name of Python module for generating tests
        - `path_runtime`(optional): User-written Python file (e.g. existing test files) that makes use of functions in the selected module.
    - Output:
        - `module_name.json`: A configuration file containing all information used to randomly generate function calls. (All function signatures and their argument types, constructor of user-defined classes, etc.) This file can be further modified by user to provide more detailed type-related information.
- **Phase 2:** Test Generation (`gen` stage)
    - Input:
        - `timeout`: Pyster terminates after `timeout` seconds.
        - `coverage`: Pyster terminates after test cases reach `coverage` code coverage rate.
        - `user_tests`(optional): If current module already has test suite, `user_tests` can be provided as a list of files so that Pyster will not generate tests covering lines already tested.
    - Output:
        - A runnable `module_nameTest.py` file containing all automatically generated unit tests as well as command-line output of coverage report.