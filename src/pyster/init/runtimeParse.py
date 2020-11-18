import inspect
import os
import sys
import traceback
import pprint


class RuntimeParser(object):

    def __init__(self, targets, path=None):
        self._caller = inspect.stack()[1][1]
        targets = set(targets)
        self.targets = targets
        self._file_names = set(map(os.path.normpath, list(map(self._get_file, targets))))
        self.path = path

    def _get_file(self, target):
        file = "Unknown File"
        try:
            if hasattr(target, "__file__"):
                file = target.__file__
            else:
                file = inspect.getfile(target)
        except:
            pass
        return file

    def _handle_call(self, code, locals_dict, args, caller=None):
        print(code.co_name)
        params = list(code.co_varnames)[:code.co_argcount]
        args_dict = dict((p,locals_dict[p]) for p in params)
        args_type = { k: str(type(v)).split("'")[1] for k, v in args_dict.items()}
        print(args_type)
        print()

    def _handle_exception(self, code, locals_dict, args, caller=None):
        pass

    def _handle_line(self, code, locals_dict, args, caller=None):
        pass

    def _handle_return(self, code, locals_dict, args, caller=None):
        pass

    def _trace(self, frame, event, args):
        handler = getattr(self, '_handle_' + event)
        event_file = frame.f_code.co_filename
        if event_file in self._file_names:
            handler(frame.f_code, frame.f_locals, args)
        return self._trace

    def parse(self):
        sys.path.insert(0, self.path)
        # user_module = __import__(module_item.module_name)
        sys.settrace(self._trace)
        # user_module.main()
        sys.settrace(None)
