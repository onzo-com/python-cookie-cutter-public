import os
import sys

from {{cookiecutter.project_slug}}.analytics.{{cookiecutter.feature_name}}.component import main
from {{cookiecutter.project_slug}}.analytics.{{cookiecutter.feature_name}}.common.setup_logging.setup_logging import setup_loggers
setup_loggers()

if __name__ == "__main__":
    ret = main(sys.argv[1:], os.environ)
    exit(ret)
