import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pilowlib",
    version = "0.1",
    author = "Calin Crisan",
    author_email = "ccrisan@gmail.com",
    description = ("Low level pure Python library for working with Raspbery PI's peripherals"),
    license = "LGPLv3",
    keywords = "raspberry-pi low-level peripherals gpio library",
    url = "https://github.com/ccrisan/pilowlib",
    packages=['pilowlib'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
)
