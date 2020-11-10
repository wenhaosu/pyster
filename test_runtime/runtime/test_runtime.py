from __future__ import absolute_import
from __future__ import print_function

import inspect
import os
import sys
import traceback
import pprint

from collections import defaultdict


class Function(object):
    def __init__(self):
        self.calls = defaultdict(list)
        self.work = []
        self.mocks = []

    def handle_call(self, code, args, typed=True):
        if typed:
            args.pop('self', None)
            args_type = { k: str(type(v)).split("'")[1] for k, v in args.items()}
            self.work.append(args_type)
            return
        self.work.append(args)

    def handle_return(self, code, args, value, typed=True):
        callArgs = self.work.pop()
        self.calls[repr(callArgs)].append((callArgs, str(type(value)).split("'")[1]))

    def add_mock(self, code, function):
        self.mocks.append((code, function))

    def __str__(self):
        return 'Function(%s)' % self.calls


class magic(object):
    _file_names = None
    _caller = "???"
    _calls = defaultdict(Function)

    def __init__(self, modulesOrClasses, generator=None, verbose=False, mock_substitutes=None, extra_imports=None):
        self._caller = inspect.stack()[1][1]
        self._file_names = list(map(os.path.normpath, list(map(self._get_file, modulesOrClasses))))
        self.modulesOrClasses = set(modulesOrClasses)
        self.verbose = verbose

    def should_test(self, code):
        return True

    def _get_file(self, moduleOrClass):
        file = self._caller
        try:
            if hasattr(moduleOrClass, "__file__"):
                file = moduleOrClass.__file__
            else:
                file = inspect.getfile(moduleOrClass)
        except:
            pass
        return file.replace('.pyc', '.py')

    def _handle_call(self, code, locals_dict, args, caller=None):
        function = self._calls[code]
        if caller:
            self._calls[caller].add_mock(code, function)
        params = list(code.co_varnames)[:code.co_argcount]
        function.handle_call(code, dict((p,locals_dict[p]) for p in params))

    def _handle_return(self, code, locals_dict, args, caller=None):
        self._calls[code].handle_return(code, locals_dict, args)

    def _handle_line(self, code, locals_dict, args, caller=None):
        pass

    def _handle_exception(self, code, locals_dict, args, caller=None):
        pass

    def __enter__(self):
        sys.settrace(self._trace)

    def __exit__(self, exception_type, value, tb):
        sys.settrace(None)
        pp = pprint.PrettyPrinter(indent=4)
        for func in self._calls:
            pp.pprint(func.co_name)
            arg_type = {k: v for k, v in self._calls[func].calls.items()}
            print(list(arg_type.values()))
            # pp.pprint(self._calls[func].calls)

        # pp.pprint(self.group_by_file(self._file_names, self._calls))

    def group_by_file(self, file_names, function_calls):
        file_names = set(file_names)
        files = defaultdict(list)
        for code, function in function_calls.items():
            file_name = os.path.normpath(code.co_filename)
            if file_name in file_names and self.should_test(code):
                files[file_name].append((code, function))
        return files

    def _trace(self, frame, event, args):
        handler = getattr(self, '_handle_' + event)
        top = frame.f_code.co_filename
        caller = frame.f_back.f_code.co_filename
        if top in self._file_names:
            handler(frame.f_code, frame.f_locals, args)
        if caller in self._file_names and top != caller:
            handler(frame.f_code, frame.f_locals, args, frame.f_back.f_code)
        return self._trace