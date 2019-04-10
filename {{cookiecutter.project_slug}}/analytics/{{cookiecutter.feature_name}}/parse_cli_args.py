from argparse import ArgumentParser


def parse_cli_args(command_line, environment):
    """
    Parses command line arguments
    :return:
    """
    parser = ArgumentParser()

    parser.add_argument(
        "--{{cookiecutter.project_slug}}",
        default=environment.get("ENV_VAR_DEFAULT", ""),
        help="An initial environment variable",
    )

    arguments = parser.parse_args(command_line)

    return arguments
