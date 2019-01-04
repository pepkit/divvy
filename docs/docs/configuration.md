
# Divvy configuration files

The `DIVCFG` computing environment configuration consists of two components: 1) The `DIVCFG` file itself, and 2) a series of template files.

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

Each compute package must point to a template file with the `submission_template` attribute. These template files are typically stored relative to the `DIVCFG` config file. Template files are taken by looper, populated with sample-specific information, and then run as scripts. Here's an example of a generic SLURM template file:

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

Template files use variables (*e.g.* `{VARIABLE}`), which will be populated independently for each sample. The variables specified in these template files (like `{LOGFILE}` or `{CORES}`) are replaced by looper when it creates a job script.

This `DIVCFG` repository comes with some commonly used templates (in the [templates](/templates) folder):

  - SLURM: [slurm_template.sub](/templates/slurm_template.sub)
  - SGE: [sge_template.sub](/templates/sge_template.sub)
  - localhost (compute locally): [localhost_template.sub](/tempaltes/localhost_template.sub)

Most users will not need to tweak the template files, but if you need to, you can also create your own templates, giving looper ultimate flexibility to work with any compute infrastructure in any environment. To create a custom template, just follow the examples and put together what you need. Then, point to your custom template in the `submission_template` attribute of a compute package in your `DIVCFG` config file. If you make a useful template, please contribute your new templates back to this repository!

### Data sources for populating template variables

What is the source of values used to populate the variables? Well, they are pooled together from several sources. Divvy uses a hierarchical system to collect data values from global and local sources, which enables you to re-use settings across projects and environments. To start, there are a few built-ins:

Built-in variables:

- `{CODE}` is a reserved variable that refers to the actual command string that will run the pipeline. `Looper` will piece together this command individually for each sample
- `{JOBNAME}` -- automatically produced by `looper` using the `sample_name` and the pipeline name.
- `{LOGFILE}` -- automatically produced by `looper` using the `sample_name` and the pipeline name.


Other variables are not automatically created by `looper` and are specified in a few different places:

*DIVCFG config file*. Variables that describes settings of a **compute environment** should go in the `DIVCFG` file. Any attributes in the activated compute package will be available to populate template variables. For example, the `partition` attribute is specified in many of our default `DIVCFG` files; that attribute is used to populate a template `{PARTITION}` variable. This is what enables pipelines to work in any compute environment, since we have no control over what your partitions are named. You can also use this to change SLURM queues on-the-fly.

*pipeline_interface.yaml*. Variables that are **specific to a pipeline** can be defined in the `pipeline interface` file. Variables in two different sections are available to templates: the `compute` and `resources` sections. The difference between the two is that the `compute` section is common to all samples, while the `resources` section varies based on sample input size. As an example of a variable pulled from the `compute` section, we defined in our `pipeline_interface.yaml` a variable pointing to the singularity or docker image that can be used to run the pipeline, like this:

```
compute:
  singularity_image: /absolute/path/to/images/image
```

Now, this variable will be available for use in a template as `{SINGULARITY_IMAGE}`. This makes sense to put in the `compute` section because it doesn't change for different sizes of input files. This path should probably be absolute, because a relative path will be interpreted as relative to the working directory where your job is executed (*not* relative to the pipeline interface).

The other pipeline interface section that is available to templates is `resources`. This section uses a list of *resource packages* that vary based on sample input size. We use these in existing templates to adjust the amount of resources we need to request from a resource manager like SLURM. For example: `{MEM}`, `{CORES}`, and `{TIME}` are all defined in this section, and they vary for different input file sizes.

[Read more about pipeline_interface.yaml here](http://looper.readthedocs.io/en/latest/pipeline-interface.html).

*project_config.yaml*. Finally, project-level variables can also be populated from the `compute` section of a project config file. We don't recommend using this and it is not yet well documented, but it would enable you to make project-specific compute changes (such as billing a particular project to a particular SLURM resource account).
