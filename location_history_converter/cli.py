"""CLI interface for location_history_converter project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""
import argparse

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
    parser = argparse.ArgumentParser()
    parser.add_argument("--geodata-file", help="the custom data source must be comma-separated with a header like in geonames cities1000.csv file")
    parser.add_argument("--location-file", help="the file with location history")
    parser.parse_args()
    print("This will do something")
