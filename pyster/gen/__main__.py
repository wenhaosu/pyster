import logging

from ..common import ConfigObject, notify_init_params, parser, check_path_valid
from .covDrivenFilter import CoverageDrivenFilter

if __name__ == "__main__":
    args = parser.parse_args()
    project_path = args.project_path
    module_name = args.module_name
    user_tests = args.user_tests
    timeout = args.timeout
    coverage_target = args.coverage

    notify_init_params(args, stage="gen")
    check_path_valid(project_path, module_name)

    try:
        config = ConfigObject(project_path, module_name)
        config.read_from_config()
        CoverageDrivenFilter(config, coverage_target, timeout, user_tests).generate()
    except Exception as e:
        logging.exception(e)
