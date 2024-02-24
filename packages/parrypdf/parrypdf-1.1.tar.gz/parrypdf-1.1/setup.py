import setuptools
from pathlib import Path

setuptools.setup(
    name="parrypdf",
    version=1.1,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["data", "tests"])
)


# --> python setup.py sdist bdist_wheel
# twine upload dist/*
