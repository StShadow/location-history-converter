"""
location_history_converter base module.

This is the principal module of the location_history_converter project.
here you put your main classes and objects.

Be creative! do whatever you want!

If you want to replace this with a Flask application run:

    $ make init

and then choose `flask` as template.
"""
import csv
import io
import logging

import reverse_geocoder as rg
from sortedcontainers import SortedDict

# example constant variable
NAME = "location_history_converter"

"""
So, long story short:

1. load file with cities
1.1 init reverse_geocoding module

2. load location history file
2.1 convert it to a list of coordinates
4. reverse coordinates one-by-one
4.1 reverse only first coordinate this day and skip the rest
4.2 add to map day<->country
5. dump map to a csv file
"""


def init_geocoder(geocode_filename=None):

    if geocode_filename is None:
        logging.info("Default geocoder will be used")
        return rg
    else:
        geocoder = Object()
        geocoder.name = "CustomGeocoder"
        geo = rg.RGeocoder(
            mode=2,
            verbose=True,
            stream=io.StringIO(
                open(geocode_filename, encoding="utf-8").read()
            ),
        )
        geocoder.search = geo.query
        logging.info(
            "Custom geocoder will be used (source file %s)"
            % (geocode_filename)
        )
        return geocoder


def dump_history_to_csv(history: SortedDict, output_file_name: str):
    if output_file_name is None or history is None:
        raise ValueError("Not all parameters are valid")
    else:
        with open(output_file_name, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Country"])
            for key, value in history.items():
                writer.writerow([str(key), value])


class Object(object):
    pass
