# <img src="img/divvy_logo.svg" class="img-header">

[![PEP compatible](http://pepkit.github.io/img/PEP-compatible-green.svg)](http://pepkit.github.io)


`Divvy` is a computing resource configuration manager. It reads a standard configuration file describing available compute resources and then uses a simple Jinja-like templating system to enable users to write custom job submission scripts.

In `divvy`, computing resources are organized as *compute packages*, which define job submission templates and other variables. Users then select a compute package and provide variable values, and `divvy` populates the templates to write compute jobs. The flexible templating system means users can quickly switch jobs to submit to any computing resource (laptop, cluster, cloud). `Divvy` provides both an interactive python API and a command-line interface.


## Installing

Releases are posted as [GitHub releases](https://github.com/databio/divvy/releases), or you can install from PyPI using `pip`:


```{console}
pip install --user divvy
```

Update `divvy` with:

```{console}
pip install --user --upgrade divvy
```


## Quick start

Use `divvy` via python interface:

```{python}
import divvy
dcc = divvy.ComputingConfiguration()
dcc.activate_package("slurm")

# write out a submission script
dcc.write_script("test_script.sub", {"code": "bowtie2 input.bam output.bam"})
```

Or via command-line:

```{console}
divvy list
divvy write --package slurm --settings myjob.yaml --sample sample1 --outfile submit_script.txt
```

To begin, check out the [tutorial](tutorial).
