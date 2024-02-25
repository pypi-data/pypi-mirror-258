from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Catch error pentaho'
LONG_DESCRIPTION = 'A package for capturing errors encountered during the data extraction process in ETL workflows using Pentaho'

# Setting up
setup(
    name="cepent",
    version=VERSION,
    author="Ysis Longart (Biwiser)",
    author_email="ysisl@biwiser.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/biwiser-com/cepent",
    packages=find_packages(),
    install_requires=['psycopg2'],
    keywords=['python', 'psycopg2', 'catch', 'pentaho'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)