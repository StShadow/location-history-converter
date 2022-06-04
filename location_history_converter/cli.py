"""CLI interface for location_history_converter project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""
import argparse
import logging

import location_history_converter.base as base


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m location_history_converter` and `$ location_history_converter `.

    This is your program's entry point.

    You can change this function to do whatever you want.
    Examples:
        * Run a test suite
        * Run a server
        * Do some other stuff
        * Run a command line application (Click, Typer, ArgParse)
        * List all available tasks
        * Run an application (Flask, FastAPI, Django, etc.)
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--geodata-file",
        help=(
            "the custom data source must be comma-separated"
            "with a header like in geonames cities1000.csv"
            "file"
        ),
    )
    parser.add_argument(
        "--location-file", help="the file with location history", required=True
    )
    parser.add_argument(
        "--output-file",
        help="the file where to put results, otherwise output.csv",
    )
    parser.add_argument(
        "--verbose",
        help="DEBUG logging level",
        action=argparse.BooleanOptionalAction,
    )
    args = parser.parse_args()
    dump_args(args)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    geocoder = base.init_geocoder(args.geodata_file)

    result = base.history_to_dict(args.location_file, geocoder)

    outfile = (
        args.output_file if args.output_file is not None else "output.csv"
    )

    base.dump_history_to_csv(result, outfile)

    logging.info("Done!")


def dump_args(args):
    for arg in vars(args):
        value = getattr(args, arg)
        logging.debug("%s=%s" % (arg, value))
