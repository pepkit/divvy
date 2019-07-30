# <img src="img/divvy_logo.svg" class="img-header"> makes software portable

[![PEP compatible](http://pepkit.github.io/img/PEP-compatible-green.svg)](http://pepkit.github.io)

## What is `divvy`?

`Divvy` is a computing resource configuration manager. It organizes available computing resources and populates templates to submit jobs so users can quickly toggle among any computing resource (laptop, cluster, cloud). `Divvy` provides both an interactive python API and a command-line interface.


## What makes `divvy` better?

<img src="img/nodivvy.svg" style="float:left; padding-left: 5px; padding-right: 25px">
Divvy *makes compute-heavy software portable*, that is, it will work on any computing environment, from a laptop to the cloud.

Many bioinformatics tools require a particular compute resource setup. For example, one pipeline may be written to require running on SLURM, while another requires a cloud provider like AWS, and yet another just runs directly on your laptop. This makes it difficult to use these tools with different computing systems.

<hr>

<img src="img/divvy-connect.svg" style="float:left; padding-left: 5px; padding-right: 25px">

Instead, `divvy` provides an interface so divvy-compatible tools can run on any computing resource. Users only need to configure their computing environment once, and all divvy-compatible tools will use this same configuration.

Divvy reads a standard configuration file describing available compute resources and then uses a simple Jinja-like template system to write custom job submission scripts. Computing resources are organized as *compute packages*, which users select, then provide variable values, and `divvy` populates the templates to write compute jobs. 

<br clear="all"/>

## Quick start

#### Install and initialize


```{console}
pip install --user divvy
export DIVCFG="divvy_config.yaml"
divvy init -c $DIVCFG
```

#### List available compute packages

```{console}
divvy list
```

```{console}
Divvy config: divvy_config.yaml

docker
default
singularity_slurm
singularity
local
slurm
```
#### Write a submission script:

```{console}
divvy write --package slurm \
	--settings myjob.yaml \
	--sample sample1 \
	--outfile submit_script.txt
```

#### Python interface

Use `divvy` via python interface:

```{python}
import divvy
dcc = divvy.ComputingConfiguration()
dcc.activate_package("slurm")

# write out a submission script
dcc.write_script("test_script.sub", {"code": "bowtie2 input.bam output.bam"})
```

To begin, check out the [tutorial](tutorial).
