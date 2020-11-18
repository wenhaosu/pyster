import sys
from runtime.test_runtime import RuntimeParser
sys.path.append('../../webpy')
from web.db import *
import web.db
import time

import typing


def main():
    param = SQLParam("name")
    q = SQLQuery(["SELECT * FROM test WHERE name="])
    p = SQLQuery(param)
    q + p


if __name__ == "__main__":
    parser = RuntimeParser([web.db, SQLParam, SQLQuery])
    sys.settrace(parser._trace)
    main()
    sys.settrace(parser._trace)
        
