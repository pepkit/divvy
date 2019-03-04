# <img src="img/divvy_logo.svg" class="img-header">

[![PEP compatible](http://pepkit.github.io/img/PEP-compatible-green.svg)](http://pepkit.github.io)


`divvy` is a simple templating system written in python that allows users to write compute jobs that can be submitted to any computing resource (laptop, cluster, cloud). It works using a simple configuration file, which we call *computing configuration files*, where you specify variables for your computing environment. It uses these variables to populate simple, Jinja-like templates to make computing job submission flexible. 


## Installing


Release versions are posted on the GitHub [divvy releases page](https://github.com/databio/divvy/releases). You can install the latest release directly from PyPI using pip:

```{console}
pip install --user divvy
```

Update `divvy` with:

```{console}
pip install --user --upgrade divvy
```


## Quick start

```{python}
import divvy
dcc = divvy.ComputingConfiguration()
dcc.activate_package("slurm")

# write out a submission script
dcc.write_script("test_script.sub", {"code": "bowtie2 input.bam output.bam"})
```

To begin, check out the [tutorial](/tutorial).
