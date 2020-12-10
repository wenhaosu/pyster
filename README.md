# Pyster
[![Build Status](https://travis-ci.com/WenhaoSu/pyster.svg?branch=main)](https://travis-ci.com/WenhaoSu/pyster) [![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Coverage Status](https://coveralls.io/repos/github/WenhaoSu/pyster/badge.svg?branch=main)](https://coveralls.io/github/WenhaoSu/pyster?branch=main)

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

## Concept
* Use built-in Python functions to obtain all methods in a Python class.
* According to the methods input, randomly generate an object instance and function arguments, with special inputs (`0`, `-1` for integers, `[]` for lists and `None` for objects also into consideration). Use `coverage.py` third-party library to get the coverage rate increment after calling the randomly generated function call.
* Repeat step 2 until we reached 100% coverage rate or the target coverage rate from user input, or the specified timeout is reached.
* Dump all auto-generated unit tests into a test file and save it into the project test suite directory, together with a before/after coverage rate of the class.
