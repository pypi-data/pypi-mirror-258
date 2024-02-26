from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

VERSION = '1.1.2'
DESCRIPTION = 'Anonymizes an Excel file and synthesizes new data in its place'

# Setting up
setup(
    name="excel-anonymizer",
    version=VERSION,
    packages=find_packages(),
    author="Siddharth Bhatia",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    keywords=['python', 'excel', 'anonymization', 'security', 'data science', 'cybersecurity'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: Unix",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Office/Business :: Financial :: Spreadsheet",
    ],
    install_requires=[
        "presidio_analyzer",
        "presidio_anonymizer",
        "pandas",
        "pyarrow",
        "faker"
    ],
    entry_points={
        "console_scripts": [
            "excel-anonymizer = excel_anonymizer.excel_anonymizer:main",
            "excel-anon = excel_anonymizer.excel_anonymizer:main",
        ],
    },
)