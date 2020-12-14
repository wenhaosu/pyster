import inspect
import os
import sys

from ..common import ConfigObject, notify, Colors


class RuntimeParser(object):
    def __init__(self, target: str, config: ConfigObject, path=None):
        self._caller = inspect.stack()[1][1]
        self.target = target
        self.path = os.path.abspath(path) if path else None
        self.config = config

    def _handle_call(self, code, locals_dict, args):
        func_name = code.co_name
        params = list(code.co_varnames)[: code.co_argcount]
        args_dict = dict((p, locals_dict[p]) for p in params)
        args_type = {k: type(v) for k, v in args_dict.items()}

        if "self" not in args_dict:
            return

        class_name = type(args_dict["self"]).__name__
        module_name = type(args_dict["self"]).__module__

        for index, value in enumerate(args_dict.values()):
            if index == 0:
                continue
            self.config.add_type_override(
                [module_name, class_name, func_name, index, value]
            )

    def _handle_exception(self, code, locals_dict, args, caller=None):
        pass

    def _handle_line(self, code, locals_dict, args, caller=None):
        pass

    def _handle_return(self, code, locals_dict, args, caller=None):
        pass

    def _trace(self, frame, event, args):
        handler = getattr(self, "_handle_" + event)
        handler(frame.f_code, frame.f_locals, args)
        return self._trace

    def parse(self):
        notify(
            "Runtime parsing module: " + self.target + "...", Colors.ColorCode.yellow
        )
        if self.path:
            path, filename = os.path.split(self.path)
            sys.path.insert(0, path)
            user_module = __import__(filename.split(".")[0])
            sys.settrace(self._trace)
            user_module.main()
            sys.settrace(None)
