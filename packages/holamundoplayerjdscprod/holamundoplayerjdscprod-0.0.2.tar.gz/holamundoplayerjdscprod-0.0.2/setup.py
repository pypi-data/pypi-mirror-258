import setuptools
from pathlib import Path

long_desc = Path("README.md").read_text()
setuptools.setup(
    name="holamundoplayerjdscprod",
    version="0.0.2",
    long_description=long_desc,
    packages=setuptools.find_packages(
        exclude=["mocks", "tests"]
    )
)
