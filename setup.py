"""Python setup.py for location_history_converter package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("location_history_converter", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="location_history_converter",
    version=read("location_history_converter", "VERSION"),
    description="Awesome location_history_converter created by StShadow",
    url="https://github.com/StShadow/location-history-converter/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="StShadow",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["location_history_converter = location_history_converter.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
)
