[logo]: img/logo_divvy.svg

# ![logo][logo] Divvy

[![PEP compatible](http://pepkit.github.io/img/PEP-compatible-green.svg)](http://pepkit.github.io)


`divvy` is a python package that provides an API for handling standardized *computing configuration files*. It enables users on different computing systems (laptop, cluster, cloud) to use the same code in any computing environment. It works using a simple configuration file, where you describe variables you need and templates. 


## Installing


Release versions are posted on the GitHub [divvy releases page](https://github.com/pepkit/divvy/releases). You can install the latest release directly from GitHub using pip:

```
pip install --user https://github.com/pepkit/divvy/zipball/master
```

Update `divvy` with:

```
pip install --user --upgrade https://github.com/divvy/caravel/zipball/master
```


## Quick start

```
import divvy
dcc = divvy.ComputingConfiguration()
dcc.activate_package("default")
dcc.compute
```



## Divvy configuration files 

Example divvy configuration files are in the [pepenv repository](https://github.com/pepkit/pepenv).




## Motivation

Originally, [looper](http://looper.readthedocs.io/) was programmed to read a `PEPENV` file, which configured shared computing resources. This capability has utility outside of `looper`, so the `divvy` package was created to abstract all the functionality originally in `PEPENV`. `Divvy` enables any third-party python package (including `looper`) to have direct access to standardized computing configuration files.

