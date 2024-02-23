
import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="kraken-localize",
    version="0.0.16",
    description="kraken-localize",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tactik8/krakenlocalize",
    author="Tactik8",
    author_email="info@tactik8.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["data/*.db", "data/*.csv", "data/*.zip"]},
    install_requires=["kraken-thing", "requests", "babel", "pint"],

)

    