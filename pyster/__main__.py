import logging

from .init.staticParse import UserModule
from .init.runtimeParse import RuntimeParser
from .gen.covDrivenFilter import CoverageDrivenFilter
from .common import ConfigObject, notify_init_params, parser, check_path_valid

if __name__ == "__main__":
    args = parser.parse_args()
    project_path = args.project_path
    module_name = args.module_name
    path_runtime = args.path_runtime
    user_tests = args.user_tests
    timeout = args.timeout
    coverage_target = args.coverage

    notify_init_params(args, stage="joint")
    check_path_valid(project_path, module_name)

    config = ConfigObject(project_path, module_name)

    try:
        module_item = UserModule(project_path, module_name, config)
        parser = RuntimeParser(config.module_name, config, path_runtime)
        parser.parse()
        config.dump_to_config()
        CoverageDrivenFilter(config, coverage_target, timeout, user_tests).generate()

    except Exception as e:
        logging.exception(e)
