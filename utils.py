import os
import argparse


def get_loggly_config_location() -> str:
    """
    Retrieves logging config file from env variable

    Returns:
        Logging File Location

    Raises:
        EnvironmentError
    """
    loggly_config_file = os.environ.get("LOGGLY_CONF_FILE")
    if not loggly_config_file:
        raise EnvironmentError("Missing logger file environment variable")
    return loggly_config_file


def parse_arguments(args: list):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--env",
        help="select environment to run",
        type=str,
        choices=["prod", "local"],
        default="local",
    )
    return parser.parse_args(args)


def get_host_and_port(env: str) -> tuple:
    if env == "local":
        return ("127.0.0.1", 1234)
    return ("0.0.0.0", 1234)
