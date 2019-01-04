# divvy python package

[![Build Status](https://travis-ci.org/pepkit/divvy.svg?branch=master)](https://travis-ci.org/pepkit/divvy) [![PEP compatible](http://pepkit.github.io/img/PEP-compatible-green.svg)](http://pepkit.github.io)

`divvy` is the official python package for reading **Portable Environment Configuration** files (**PEC**s) in `python`. 

Links to complete documentation:

* Complete documentation and API for the `divvy` python package is at [divvy.readthedocs.io](http://divvy.readthedocs.io/).
* Reference documentation for standard **PEP** format is at [pepkit.github.io](https://pepkit.github.io/).
* Example PEPs for testing `divvy` are in the [pepenv repository](https://github.com/pepkit/pepenv).

# Quick start

```
import divvy, os
divvy.setup_divvy_logger("DEBUG", devmode=True)
dcc = divvy.ComputingConfiguration(os.path.expandvars("$PEPENV"))
dcc.activate_compute_package("default")
```

# Motivation

Originally, [looper](http://looper.readthedocs.io/) was programmed to read a `PEPENV` file, which configured shared computing resources. This capability has utility outside of `looper`, so the `divvy` package was created to abstract all the functionality originally in `PEPENV`. `Divvy` enables any third-party python package (including `looper`) to have direct access to standardized computing configuration files.

# Contributing

Contributions are welcome! For bug reports, feature requests, or questions, please use the [GitHub issue tracker](https://github.com/pepkit/divvy/issues). Please submit pull requests to the `dev` branch on the primary repository at http://github.com/pepkit/divvy.
