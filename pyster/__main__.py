import os

from .common import parser

if __name__ == "__main__":
    args = parser.parse_args()
    project_path = args.project_path
    module_name = args.module_name
    path_runtime = args.path_runtime
    user_tests = args.user_tests
    timeout = args.timeout
    coverage_target = args.coverage

    pr = " --path_runtime " + path_runtime if path_runtime != "" else ""

    os.system(
        "python3 -m pyster.init --project_path "
        + project_path
        + " --module_name "
        + module_name
        + pr
    )
    os.system(
        "python3 -m pyster.gen --project_path "
        + project_path
        + " --module_name "
        + module_name
        + " --user_tests "
        + " ".join(t for t in user_tests)
        + " -t "
        + str(timeout)
        + " -c "
        + str(coverage_target)
    )
