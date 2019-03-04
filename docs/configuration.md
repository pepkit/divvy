
# Divvy configuration files

## The `$DIVCFG` environment variable

At the heart of `divvy` is a `yaml` configuration file that specifies your available `compute_package`s. Each package represents a computing resource; for example, by default we have 1 package (called `local`) that populates templates to simple run jobs in the local console, and another package (called `slurm`) with a generic template to submit jobs to the SLURM cluster resource manager. You can customize your compute packages as much as you need. 

The file specifying the compute packages is called the `DIVCFG` file. If using `divvy` from within `python`, you can pass a configuration file when you construct a new `ComputingConfiguration` object. If you don't specify one, `divvy` will first look for a file in the `$DIVCFG` environment variable. If it cannot find one there, then it will load a default configuration file with a few basic compute packages.

## The DIVCFG file

The DIVCFG file is a `yaml` file listing different *compute packages*. Consider an example environment configuration file:

```{yaml}
compute_packages:
  default:
    submission_template: templates/local_template.sub
    submission_command: sh
  local:
    submission_template: templates/local_template.sub
    submission_command: sh
  develop_package:
    submission_template: templates/slurm_template.sub
    submission_command: sbatch
    partition: develop
  big:
    submission_template: templates/slurm_template.sub
    submission_command: sbatch
    partition: bigmem
```

The sub-sections below `compute_packages` each define a *compute package* that can be activated. `Divvy` uses these compute packages to determine how to submit your jobs. By default, `divvy` uses the package named `default`. You can make your default whatever you like. You can activate any other compute package __on the fly__ by specifying using the `activate_package` function.

You can make as many compute packages as you wish, and name them whatever you wish. You can also add whatever attributes you like to the compute package. Each compute package must specify the `submission_command` and `submission_template` attributes. 

### The `submission_command` attribute

The `submission_command` attribute is the string your cluster resource manager uses to submit a job. In this example, we're using the SLURM command `sbatch`. Looper will run our jobs as: `sbatch submission_script.txt`. This flexibility is what enables looper to work with any cluster resource manager.

### The `submission_template` attribute

Each compute package specifies a path to a template file (`submission_template`). These paths can be relative or absolute; relative paths are considered *relative to the DIVCFG file*.


## Template files

Each compute package must point to a template file with the `submission_template` attribute. These template files are typically stored relative to the `DIVCFG` config file. Template files are taken by `divvy`, populated with job-specific information, and then run as scripts. Here's an example of a generic SLURM template file:

```{bash}
#!/bin/bash
#SBATCH --job-name='{JOBNAME}'
#SBATCH --output='{LOGFILE}'
#SBATCH --mem='{MEM}'
#SBATCH --cpus-per-task='{CORES}'
#SBATCH --time='{TIME}'
#SBATCH --partition='{PARTITION}'
#SBATCH -m block
#SBATCH --ntasks=1

echo 'Compute node:' `hostname`
echo 'Start time:' `date +'%Y-%m-%d %T'`

srun {CODE}
```

Template files use variables (*e.g.* `{VARIABLE}`), which will be populated independently for each job.

This `DIVCFG` repository comes with some commonly used templates (in the [templates](/templates) folder):

  - SLURM: [slurm_template.sub](/templates/slurm_template.sub)
  - SGE: [sge_template.sub](/templates/sge_template.sub)
  - localhost (compute locally): [localhost_template.sub](/tempaltes/localhost_template.sub)

Most users will not need to tweak the template files, but if you need to, you can also create your own templates, giving `divvy` ultimate flexibility to work with any compute infrastructure in any environment. To create a custom template, just follow the examples and put together what you need. Then, point to your custom template in the `submission_template` attribute of a compute package in your `DIVCFG` config file.

