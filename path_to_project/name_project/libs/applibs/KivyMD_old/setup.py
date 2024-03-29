import sys

assert sys.version_info >= (3, 5, 0), "KivyMD requires Python 3.5+"

from setuptools import setup
from os.path import join, dirname
import re


def get_version() -> str:
    version_file = join(dirname(__file__), "kivymd/__init__.py")
    version_file_data = open(version_file, "rt", encoding="utf-8").read()
    version_regex = r"(?<=^__version__ = ['\"])[^'\"]+(?=['\"]$)"
    try:
        version = re.findall(version_regex, version_file_data, re.M)[0]
        return version
    except IndexError:
        raise ValueError(f"Unable to find version string in {version_file}.")


# Static strings are in setup.cfg
setup(
    version=get_version(),
    packages=["kivymd"],
    package_dir={"kivymd": "kivymd"},
    package_data={
        "kivymd": [
            "uix/*.py",
            "utils/*.py",
            "behaviors/*.py",
            "toast/*.py",
            "toast/kivytoast/*.py",
            "toast/androidtoast/*.py",
            "stiffscroll/*.py",
            "vendor/*.py",
            "vendor/circleLayout/*.py",
            "vendor/circularTimePicker/*.py",
            "vendor/navigationdrawer/*.py",
            "images/*.png",
            "images/*.jpg",
            "images/*.atlas",
            "fonts/*.ttf",
        ]
    },
    extras_require={},
    install_requires=["kivy", "pillow", "requests"],
    setup_requires=[],
    python_requires=">=3.5",
)
