#! /usr/bin/env python

import os
from setuptools import setup
import sys

PACKAGE = "divvy"

# Additional keyword arguments for setup().
extra = {}

# Ordinary dependencies
DEPENDENCIES = []
with open("requirements/requirements-all.txt", "r") as reqs_file:
    for line in reqs_file:
        if not line.strip():
            continue
        # DEPENDENCIES.append(line.split("=")[0].rstrip("<>"))
        DEPENDENCIES.append(line)

# numexpr for pandas
try:
    import numexpr
except ImportError:
    # No numexpr is OK for pandas.
    pass
else:
    # pandas 0.20.2 needs updated numexpr; the claim is 2.4.6, but that failed.
    DEPENDENCIES.append("numexpr>=2.6.2")

extra["install_requires"] = DEPENDENCIES

with open("{}/_version.py".format(PACKAGE), "r") as versionfile:
    version = versionfile.readline().split()[-1].strip("\"'\n")

# Handle the pypi README formatting.
try:
    import pypandoc

    long_description = pypandoc.convert_file("README.md", "rst")
except (IOError, ImportError, OSError):
    long_description = open("README.md").read()

setup(
    name=PACKAGE,
    packages=[PACKAGE],
    version=version,
    description="A python-based configuration manager for portable environment configurations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: System :: Distributed Computing",
    ],
    keywords="project, metadata, bioinformatics, sequencing, ngs, workflow",
    url="https://github.com/pepkit/{}/".format(PACKAGE),
    author=u"Nathan Sheffield, Vince Reuter, Michal Stolarczyk",
    author_email=u"nathan@code.databio.org, vreuter@virginia.edu, mjs5kd@virginia.edu",
    license="BSD-2-Clause",
    entry_points={
        "console_scripts": ["divvy = divvy.__main__:main"],
    },
    package_data={"divvy": [os.path.join("divvy", "*")]},
    include_package_data=True,
    test_suite="tests",
    tests_require=(["mock", "pytest"]),
    setup_requires=(
        ["pytest-runner"] if {"test", "pytest", "ptr"} & set(sys.argv) else []
    ),
    **extra
)
