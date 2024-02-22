import argparse
import importlib_resources
from bin.cli_impl import *
from rich import print, inspect, print_json
from rich.rule import Rule
from rich.panel import Panel
from rich.padding import Padding
from rich.logging import RichHandler
from rich.console import Console
from rich.markdown import Markdown
from rich.traceback import install
from .parsers.formatter import RichHelpFormatterCitros

install()

from bin import __version__ as citros_version

from .parsers import (
    parser_run,
    parser_init,
    parser_data,
    parser_service,
    parser_report,
    parser_launch,
    parser_parameter,
    parser_simulation,
)


# PANNEL = ""
PANNEL = Panel.fit(
    f"""[green]████████████████████████████████████████████████████████████
██      ███        ██        ██       ████      ████      ██
█  ████  █████  ████████  █████  ████  ██  ████  ██  ███████
█  ███████████  ████████  █████       ███  ████  ███      ██
█  ████  █████  ████████  █████  ███  ███  ████  ████████  █
██      ███        █████  █████  ████  ███      ████      ██
████████████████████████████████████████████████████████████""",
    subtitle=f"[{citros_version}]",
)


def epilog(url="https://docs.citros.io"):
    return Panel(Markdown(f"Read more at `{url}`"))


def main():
    description_path = "citros.md"

    # main parser -----------------------------------------
    parser = argparse.ArgumentParser(
        description=Panel(
            Markdown(
                open(
                    importlib_resources.files(f"data.doc.cli").joinpath(
                        description_path
                    ),
                    "r",
                ).read()
            ),
            subtitle=f"[{citros_version}]",
            title="description",
        ),
        epilog=epilog(),
        formatter_class=RichHelpFormatterCitros,
        # add_help=False
    )

    parser.add_argument(
        "-dir", "--dir", default=".", help="The working dir of the project"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="set logging level to debug"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="use verbose console prints"
    )
    parser.add_argument("-V", "--version", action="version", version=citros_version)
    parser.set_defaults(func=citros)

    def func(args, argv):
        print(PANNEL)
        citros(args, argv)

    parser.set_defaults(func=func)

    subparsers = parser.add_subparsers(
        title="commands",
        help="citros commands",
        dest="type",  # required=True
    )

    parser_init(
        subparsers,
        epilog("https://docs.citros.io/docs/next/commands/init"),
    )
    parser_run(
        subparsers,
        epilog("https://docs.citros.io/docs/next/commands/run"),
    )
    parser_data(
        subparsers,
        epilog("https://docs.citros.io/docs/next/commands"),
    )
    parser_report(
        subparsers,
        epilog(),
    )
    # parser_service(
    #     subparsers,
    #     epilog(),
    # )

    # parser_simulation(
    #     subparsers,
    #     epilog(),
    # )
    # parser_parameter(
    #     subparsers,
    #     epilog(),
    # )
    # parser_launch(
    #     subparsers,
    #     epilog(),
    # )

    args, argv = parser.parse_known_args()

    args.func(args, argv)


if __name__ == "__main__":
    main()
