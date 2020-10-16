# Pyster

Pyster is a coverage-driven automatic unit test generator for Python projects.

## Usage
```bash
python3 src/pyster <dir-to-python-module>
```

## TODO List
- [ ] Use built-in Python functions to obtain all methods in a Python class.
- [ ] According to the methods input, randomly generate an object instance and function arguments, with special inputs (`0`, `-1` for integers, `[]` for lists and `None` for objects also into consideration). Use `coverage.py` third-party library to get the coverage rate increment after calling the randomly generated function call.
- [ ] Repeat step 2 until we reached 100% coverage rate or the target coverage rate from user input, or the specified timeout is reached.
- [ ] Dump all auto-generated unit tests into a test file and save it into the project test suite directory, together with a before/after coverage rate of the class.
