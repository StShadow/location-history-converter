import location_history_converter.base as base
import tempfile
from _pytest.tmpdir import tmp_path


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
    assert geocoder.name == "CustomerGeocoder"


#    with tempfile.NamedTemporaryFile() as tmp:
#        print(tmp.name)
#        tmp.write(b'this is some content')
#        tmp.flush()
#        tmp.seek(0)
#        geocoder = base.init_geocoder(tmp.name)
#        assert geocoder.__name__ == "Object"
