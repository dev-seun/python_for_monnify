from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.6'
DESCRIPTION = 'Monnify payment module for python developer'
LONG_DESCRIPTION = 'This package allow you to connnect to monnify payment gateway with ease, and perform most of monnify payment solution offered'

# Setting up
setup(
    name="py_monnify",
    version=VERSION,
    author="Smarttek",
    fullname="Oladele seun",
    author_email="<samwhitedove@gmail.com>",
    maintainer="smarttek",
    maintainer_email="samwhitedove@gmail.com",
    url="https://github.com/samwhitedove/python_for_monnify",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests'],
    requires_python = ">=3.7",
    keywords=['python', 'payment', 'gateway', 'monnify', 'payment gateway'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    license= "OSI Approved :: MIT License",
    download_url= "https://github.com/samwhitedove/python_for_monnify",

)
