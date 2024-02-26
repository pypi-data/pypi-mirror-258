from setuptools import find_packages
from setuptools import setup
import pathlib


with open("README.md") as file:
    long_description = file.read()


with open("requirements.txt") as file:
    requirements = file.read()


setup(
    name="dbn4_clinic",
    version="0.3.0",
    packages=find_packages(),
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
)
