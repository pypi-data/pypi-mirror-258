import argparse

from puffling.cli.build import build_command
from puffling.cli.dep import dep_command
from puffling.cli.metadata import metadata_command
from puffling.cli.version import version_command


def puffling() -> int:
    parser = argparse.ArgumentParser(prog="puffling", allow_abbrev=False)
    subparsers = parser.add_subparsers()

    defaults = {"metavar": ""}

    build_command(subparsers, defaults)
    dep_command(subparsers, defaults)
    metadata_command(subparsers, defaults)
    version_command(subparsers, defaults)

    kwargs = vars(parser.parse_args())
    try:
        command = kwargs.pop("func")
    except KeyError:
        parser.print_help()
    else:
        command(**kwargs)

    return 0
