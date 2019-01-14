[logo]: img/logo_divvy.svg

# ![logo][logo] Divvy

[![PEP compatible](http://pepkit.github.io/img/PEP-compatible-green.svg)](http://pepkit.github.io)


`divvy` is a simple templating system written in python that allows users to write compute jobs that can be submitted to any computing resource (laptop, cluster, cloud). It works using a simple configuration file, which we call *computing configuration files*, where you specify variables for your computing environment. It uses these variables to populate simple, Jinja-like templates to make computing job submission flexible. 


## Installing


Release versions are posted on the GitHub [divvy releases page](https://github.com/pepkit/divvy/releases). You can install the latest release directly from PyPI using pip:

```
pip install --user divvy
```

Update `divvy` with:

```
pip install --user --upgrade divvy
```


## Quick start

```
import divvy
dcc = divvy.ComputingConfiguration()
dcc.activate_package("default")
dcc.compute
```

## Motivation

Originally, [looper](http://looper.readthedocs.io/) was programmed to read a `PEPENV` file, which configured shared computing resources. This capability has utility outside of `looper`, so the `divvy` package was created to abstract all the functionality originally in `PEPENV`. `Divvy` enables any third-party python package (including `looper`) to have direct access to standardized computing configuration files.

