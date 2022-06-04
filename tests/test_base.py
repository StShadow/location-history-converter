import location_history_converter.base as base
import pytest
import csv
from sortedcontainers import SortedDict
from datetime import date
import os
import logging
import ijson


@pytest.fixture(autouse=True)
def run_around_tests():
    logging.basicConfig(level=logging.DEBUG)
    yield


def test_base():
    assert base.NAME == "location_history_converter"


def test_init_default_geocoder():
    geocoder = base.init_geocoder()
    assert geocoder.__name__ == "reverse_geocoder"


def test_init_customer_geocoder(tmp_path):
    tmp_file = tmp_path / "myfile"
    tmp_file.touch()
    tmp_file.write_text(
        "lat,lon,name,admin1,admin2,cc\n42.57952,1.65362,El Tarter,Canillo,,AD",
        encoding="utf-8",
    )
    print(tmp_file.name)
    geocoder = base.init_geocoder(tmp_file)
    assert geocoder.name == "CustomGeocoder"


def test_dump_history_to_csv_when_no_file():
    with pytest.raises(Exception):
        base.dump_history_to_csv(None, None)


def test_dump_history_to_csv_when_random_order(tmp_path):
    tmp_file = tmp_path / "myfile"

    csv_rowlist = [
        ["Date", "Country"],
        ["2022-01-05", "PL"],
        ["2022-02-03", "CZ"],
        ["2022-05-03", "SK"],
    ]

    history = SortedDict(
        {
            date(2022, 1, 5): "PL",
            date(2022, 5, 3): "SK",
            date(2022, 2, 3): "CZ",
        }
    )
    base.dump_history_to_csv(history, tmp_file)

    assert os.path.getsize(tmp_file) > 0

    with open(tmp_file, "r") as file:
        reader = csv.reader(file)
        rows = 0
        for idx, row in enumerate(reader):
            logging.debug(row)
            assert row[1] == csv_rowlist[idx][1]
            rows = rows + 1
        assert rows == len(csv_rowlist)


FIXTURE_DIR = os.path.join(os.path.realpath(__file__), "..")


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "test-location.json"))
def test_record_to_dictionary_item_conversion(datafiles):
    for file in datafiles.listdir():
        with open(file, "rb") as f:
            for record in ijson.items(f, "locations.item"):
                date = record["timestamp"][0:10]
                assert date.startswith("2011") == True


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "test-location.json"))
def test_history_to_2_arrays(datafiles):
    file = datafiles.listdir()[0]
    (dates, locations) = base.history_to_arrays(file)
    assert len(dates) == 2
    assert len(locations) == 2
    assert len(locations[0]) == 2
    for date in dates:
        assert date.year == 2011

@pytest.mark.skip(reason="No way of currently testing multiprocessing code")
def test_coordinates_to_country():
    geocoder = base.init_geocoder()
    lat = 414039706
    lon = 21993300
    country = base.coordinates_to_country(lat, lon, geocoder)

    assert country == "ES"
