from {{cookiecutter.project_slug}}.analytics.{{cookiecutter.feature_name}}.parse_cli_args import parse_cli_args
from {{cookiecutter.project_slug}}.analytics.{{cookiecutter.feature_name}}.common.setup_logging.setup_logging import initialise_logging


def main(command_line, environment):
    args = parse_cli_args(command_line, environment)
    if args is None:
        return 1

    initialise_logging(args.debug)