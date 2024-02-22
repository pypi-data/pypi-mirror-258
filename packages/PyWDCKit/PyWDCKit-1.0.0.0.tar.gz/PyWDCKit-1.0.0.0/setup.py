from setuptools import setup, find_packages
import os
from PyWDCKit import VERSION

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

DESCRIPTION = "UNOFFICIAL Python bindings for Western Digital's WDCKit drive utility"

# Setting up
setup(
    name="PyWDCKit",
    version=VERSION,
    author="mohamed-fazal-wdc (Mohamed Farhan Fazal)",
    author_email="mohamed.fazal@wdc.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['logging','pywin32'],
    url="https://github.com/mohamed-fazal-wdc/lib_wdckit",
    project_urls={
        "Bug Tracker": "https://github.com/mohamed-fazal-wdc/lib_wdckit/issues",
    },
    keywords=['python', 'wdckit', 'Western Digital', 'Sandisk',"NVMe", "SATA", "NVMe M.2", "SSD", "HDD"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "License :: Freeware"
    ]
)