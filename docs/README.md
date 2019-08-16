# <img src="img/divvy_logo.svg" class="img-header"> makes software portable

[![PEP compatible](https://pepkit.github.io/img/PEP-compatible-green.svg)](http://pepkit.github.io)

## What is `divvy`?

`Divvy` is a computing resource configuration manager. It organizes your computing resources and populates job submission templates. It makes it easy for users to toggle among any computing resource (laptop, cluster, cloud). `Divvy` provides both an interactive python API and a command-line interface.


## What makes `divvy` better?

<img src="img/nodivvy.svg" style="float:left; padding-left: 5px; padding-right: 25px">
Divvy *makes compute-heavy software portable*, so it works on any computing environment, from laptop to cloud.

Many bioinformatics tools require a particular compute resource setup. For example, one pipeline requires SLURM, another requires AWS, and yet another just runs directly on your laptop. This makes it difficult to transfer to different environments. For tools that can run in multiple environments, each one must be configured separately.

<hr>

<img src="img/divvy-connect.svg" style="float:left; padding-left: 5px; padding-right: 25px">

Instead, `divvy`-compatible tools can run on any computing resource. **Users configure their computing environment once, and all divvy-compatible tools will use this same configuration.**

Divvy reads a standard configuration file describing available compute resources and then uses a simple Jinja-like template system to write custom job submission scripts. Computing resources are organized as *compute packages*, which users select, populate with values, and build scripts for compute jobs. 

<br clear="all"/>

## Quick start

Install with:

```{console}
pip install --user divvy
```

Use the default compute packages or [configure your own](configuration.md).  See what's available:

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

<img src="img/divvy-merge.svg" style="float:right; padding-left: 25px; padding-right: 5px">

Divvy will take variables from a file or the command line, merge these with environment settings to create a specific job script. Write a submission script from the command line:

```{console}
divvy write --package slurm \
	--settings myjob.yaml \
	--sample sample1 \
	--outfile submit_script.txt
```

### Python interface

You can also use `divvy` via python interface, or you can use it to make your own python tools divvy-compatible:

```{python}
import divvy
dcc = divvy.ComputingConfiguration()
dcc.activate_package("slurm")

# write out a submission script
dcc.write_script("test_script.sub", 
	{"code": "bowtie2 input.bam output.bam"})
```

For more details, check out the [tutorial](tutorial).
