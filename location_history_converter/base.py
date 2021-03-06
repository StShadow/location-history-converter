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
from datetime import datetime

import ijson
import reverse_geocoder as rg
from sortedcontainers import SortedDict

# example constant variable
NAME = "location_history_converter"

# the way how google converts float coordinates to integer - multiple by 10e6
MULTIPLIER = 10e6

"""
So, long story short:

1. load file with cities
1.1 init reverse_geocoding module

2. load location history file
2.1 convert it to a list of coordinates
4. reverse coordinates one-by-one
4.1 reverse only first coordinate this day and skip the rest
4.2 add to map day<->country
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


"""
5. dump map to a csv file
"""


def dump_history_to_csv(history: SortedDict, output_file_name: str):
    if output_file_name is None or history is None:
        raise ValueError("Not all parameters are valid")
    else:
        with open(output_file_name, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Country"])
            for key, value in history.items():
                writer.writerow([str(key), value])


def history_to_arrays(history_file):
    dates = list()
    locations = list()
    already_processed = set()

    with open(history_file, "rb") as f:
        for record in ijson.items(f, "locations.item"):
            date_str = record["timestamp"][0:10]
            if date_str not in already_processed:
                already_processed.add(date_str)

                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                dates.append(date)

                lat = int(record["latitudeE7"]) / MULTIPLIER
                lon = int(record["longitudeE7"]) / MULTIPLIER
                locations.append((lat, lon))
                logging.info("Process day %s" % (date_str))

    logging.info("%s locations processed" % (len(dates)))
    return (dates, locations)


def arrays_to_dictionary(dates: list, locations: list, geocoder) -> SortedDict:
    BATCH = 64
    start = 0
    date_to_country = SortedDict()
    while start < len(dates):
        end = start + BATCH if start + BATCH < len(dates) else len(dates)
        logging.info("Process slice %s %s" % (start, end))
        tmp_dates = dates[start:end]
        tmp_locations = locations[start:end]
        countries = coordinates_to_country(tmp_locations, geocoder)

        for index, item in enumerate(countries):
            date_to_country[tmp_dates[index]] = item

        start = end
    logging.info("Finish processing locations")
    return date_to_country


def coordinates_to_country(latlon: list, geocoder) -> list:
    addresses = geocoder.search(latlon)
    return list(map(lambda address: address.get("cc"), addresses))


class Object(object):
    pass


def convert_location(record, geocoder):
    pass
