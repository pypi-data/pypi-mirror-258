#!/usr/bin/env python

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name="pymakima",
      version="0.1.1",
      description="Asynchronous DNS Brute Forcer by irisdotsh",
      author="Iris Blankenship",
      author_email="iris@netwatchr.com",
      license="GNU GPL v3",
      keywords=["makima", "async", "dns", "brute", "force", "security"],
      url="https://github.com/irisdotsh/makima",
      packages=["makima", "tests"],
      long_description=read("README.md"),
      entry_points={
          "console_scripts": [
              "makima=makima:main"
          ]
      },
      classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Security"])
