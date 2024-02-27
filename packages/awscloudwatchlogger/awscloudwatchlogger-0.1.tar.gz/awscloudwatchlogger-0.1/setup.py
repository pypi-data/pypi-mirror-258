from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1'
DESCRIPTION = 'Logging into aws cloudwatch from python apps'
LONG_DESCRIPTION = 'A package that allows to log into cloudwatch from python.'

# Setting up
setup(
    name="awscloudwatchlogger",
    version=VERSION,
    author="Babasaheb Pinjar",
    author_email="babasahebpinjar@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/plain",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['boto3'],
    keywords=['python', 'logger', 'cloudwatch'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
