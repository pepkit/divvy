# 1. Overview of PEP environment configuration

PEPENV is a repository that contains configuration files that describe computing environments. We refer to this as a *computing environment configuration*. Its primary use is to configure different computing options for the [looper](http://looper.readthedocs.io) pipeline submission engine. PEPENV enables `looper` to use cluster resource manager (SGE, SLURM, *etc.*) or with linux containers (`docker`, `singularity`, *etc.*). This repository provides templates to help you set up cluster computing, containerized computing, or both.

# 2. Setting up your environment

## Plugging into a compute environment where PEPENV is already deployed

For server environments where `looper` is being actively used, this repository already contains plug-and-play configuration files. If you're lucky enough to be at one of these places, set-up is very simple. Here's a list of pre-configured computing environments:

   * `uva_rivanna.yaml`: [Rivanna cluster](http://arcs.virginia.edu/rivanna) at University of Virginia
   * `cemm.yaml`: Cluster at the Center for Molecular Medicine, Vienna
   * `nih_biowulf2.yaml`: [Biowulf2](https://hpc.nih.gov/docs/userguide.html) cluster at the NIH
   * `stanford_sherlock.yaml`: [Sherlock](http://sherlock.stanford.edu/mediawiki/index.php/Current_policies) cluster at Stanford
   * `ski-cer_lilac.yaml`: *lilac* cluster at Memorial Sloan Kettering
   * `local_containers.yaml`: A generic local desktop or server (with no cluster management system) that will use docker or singularity containers.

To set up your looper to use cluster resources at one of these locations, all you have to do is:

1. Clone this repository
2. Point the `$PEPENV` environment variable to the appropriate config file by executing this command:
	```
	export PEPENV=path/to/compute_config.yaml
	```
 	(Add this line to your `.profile` or `.bashrc` if you want it to persist).

And that's it, you're done! If the existing config files do not fit your environment, you will need to create a PEPENV config file to match your environment by following these instructions:

## Configuring a new environment

To configure a new environment, we'll follow the same steps, but just point at the default file, `compute_config.yaml`, which we will then edit to match your local computing environment.

1. Clone this repository
2. Point the `$PEPENV` environment variable to the **default config file** by executing this command:
  ```
  export PEPENV=path/to/compute_config.yaml
  ```
  (Add this line to your `.profile` or `.bashrc` if you want it to persist).

3. Next, use this file as a starting point to configure your environment. If you're using SLURM and you're lucky, the only thing you will need to change is the `partition` variable, which should reflect your submission queue or partition name used by your cluster resource manager. To make more advanced changes, the documentation below will guide you through all components of the configuration.

4. Once you have it working, consider submitting your configuration file back to this repository with a pull request.


# 3. PEPENV configuration explained

The `PEPENV` computing environment configuration consists of two components: 1) The `PEPENV` file itself, and 2) a series of template files.

## The PEPENV file

The PEPENV file is a `yaml` file listing different *compute packages*. Consider an example environment configuration file:

```
compute:
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

The sub-sections below `compute` each define a *compute package* that can be activated. Looper uses these compute packages to determine how to submit your jobs. By default, looper uses the package named `default`. You can make your default whatever you like. You can instruct looper to use any other compute package __on the fly__ by specifying the `--compute` argument to `looper run` like so:

```
looper run --compute PACKAGE
```

For example, to use the `develop` partition, you would use  `looper run --compute develop_package`; to use the `bibmem` partition, use `--compute big`. You can make as many compute packages as you wish, and name them whatever you wish. You can also add whatever attributes to the compute package. They should at least have `submission_template` and `submission_command`, but you can also add other variables which could populate parts of your templates. Each compute package specifies a path to a template file (`submission_template`). These paths can be relative or absolute; relative paths are considered *relative to the pepenv file*.

The `submission_command` attribute is the string your cluster resource manager uses to submit a job. In this example, we're using the SLURM command `sbatch`. Looper will run our jobs as: `sbatch submission_script.txt`. This flexibility is what enables looper to work with any cluster resource manager.

## Template files

Each compute package must point to a template file. These template files are typically stored relative to the PEPENV config file. Template files are taken by looper, populated with sample-specific information, and then run as scripts. Here's an example of a generic SLURM template file:

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

This `pepenv` repository comes with some commonly used templates (in the [templates](/templates) folder):
* SLURM: [slurm_template.sub](/templates/slurm_template.sub)
* SGE: [sge_template.sub](/templates/sge_template.sub)
* localhost (compute locally): [localhost_template.sub](/tempaltes/localhost_template.sub)

Most users will not need to tweak the template files, but if you need to, you can also create your own templates, giving looper ultimate flexibility to work with any compute infrastructure in any environment. To create a custom template, just follow the examples and put together what you need. Then, point to your custom template in the `submission_template` attribute of a compute package in your `pepenv` config file. If you make a useful template, please contribute your new templates back to this repository!

### The source of the values

What is the source of values used to populate the variables? Well, they are pooled together from several sources. To start, there are a few built-ins:

Built-in variables:
- `{CODE}` is a reserved variable that refers to the actual command string that will run the pipeline. Looper will piece together this command individually for each sample
- `{JOBNAME}` -- automatically produced by looper using the `sample_name` and the pipeline name.
- `{LOGFILE}` -- automatically produced by looper using the `sample_name` and the pipeline name.


Other variables are not automatically created by `looper` and are specified in a few different places:

*PEPENV config file*. Variables that describes settings of a **compute environment** should go in the `PEPENV` file. Any attributes in the activated compute package will be available to populate template variables. For example, the `partition` attribute is specified in many of our default `PEPENV` files; that attribute is used to populate a template `{PARTITION}` variable. This is what enables pipelines to work in any compute environment, since we have no control over what your partitions are named. You can also use this to change SLURM queues on-the-fly.

*pipeline_interface.yaml*. Variables that are **specific to a pipeline** can be defined in the `pipeline interface` file. Variables in two different sections are available to templates: the `compute` and `resources` sections. The difference between the two is that the `compute` section is common to all samples, while the `resources` section varies based on sample input size. As an example of a variable pulled from the `compute` section, we defined in our `pipeline_interface.yaml` a variable pointing to the singularity or docker image that can be used to run the pipeline, like this:

```
compute:
  singularity_image: /absolute/path/to/images/image
```

Now, this variable will be available for use in a template as `{SINGULARITY_IMAGE}`. This makes sense to put in the `compute` section because it doesn't change for different sizes of input files. This path should probably be absolute, because a relative path will be interpreted as relative to the working directory where your job is executed (*not* relative to the pipeline interface).

The other pipeline interface section that is available to templates is `resources`. This section uses a list of *resource packages* that vary based on sample input size. We use these in existing templates to adjust the amount of resources we need to request from a resource manager like SLURM. For example: `{MEM}`, `{CORES}`, and `{TIME}` are all defined in this section, and they vary for different input file sizes.

[Read more about pipeline_interface.yaml here](http://looper.readthedocs.io/en/latest/pipeline-interface.html).

*project_config.yaml*. Finally, project-level variables can also be populated from the `compute` section of a project config file. We don't recommend using this and it is not yet well documented, but it would enable you to make project-specific compute changes (such as billing a particular project to a particular SLURM resource account).


# 4. Using docker or singularity containers

The `PEPENV` framework is a natural way to run commands in a container. All we need to do is 1) design a template that will run the job in the container, instead of natively; and 2) create a new compute package that will use that template. **To use containers with looper requires `looper`version >= 0.9**.

## 4.1 A template for container runs

This repository includes templates for the following scenarios:

- singularity on SLURM: [slurm_singularity_template.sub](templates/slurm_singularity_template.sub)
- singularity on localhost: [localhost_singularity_template.sub](templates/localhost_singularity_template.sub)
- docker on localhost: [localhost_singularity_template.sub](templates/localhost_singularity_template.sub)

If you need a different system, looking at those examples should get you started toward making your own. To take a quick example, using singularity on SLURM combines the basic SLURM script template with these lines to execute the run in container:

```
singularity instance.start {SINGULARITY_ARGS} {SINGULARITY_IMAGE} {JOBNAME}_image
srun singularity exec instance://{JOBNAME}_image {CODE}
singularity instance.stop {JOBNAME}_image
```

This template uses a few of the automatic variables defined earlier (`JOBNAME` and `CODE`) but adds two more: `{SINGULARITY_ARGS}` and `{SINGULARITY_IMAGE}`. For the *image*, this should point to a singularity image that could vary by pipeline, so it makes most sense to define this variable in the `pipeline_interface.yaml` file. So, any pipeline that provides a container should probably include a `compute: singularity_image:` attribute providing a place to point to the appropriate container image.

Of course, you will also need to make sure that you have access to `singularity` command from the compute nodes; on some clusters, you may need to add a `module load singularity` (or some variation) to enable it.

The `{SINGULARITY_ARGS}` variable comes just right after the `instance.start` command, and can be used to pass any command-line arguments to singularity. We use these, for example, to bind host disk paths into the container. **It is critical that you explicitly bind any file systems with data necessary for the pipeline so the running container can see those files**. The [singularity documentation](https://singularity.lbl.gov/docs-mount#specifying-bind-paths) explains this, and you can find other arguments detailed there. Because this setting describes something about the computing environment (rather than an individual pipeline or sample), it makes most sense to put it in the `PEPENV` environment configuration file. The next section includes examples of how to use `singularity_args`.

## 4.2 Adding compute packages for container runs.

To add a package for these templates to a `PEPENV` file, we just add a new section. There are a few examples in this repository. A singularity example we use at UVA looks like this:

```
singularity_slurm:
  submission_template: templates/slurm_singularity_template.sub
  submission_command: sbatch
  singularity_args: --bind /sfs/lustre:/sfs/lustre,/nm/t1:/nm/t1
singularity_local:
  submission_template: templates/localhost_singularity_template.sub
  submission_command: sh
  singularity_args: --bind /ext:/ext
```

These singularity compute packages look just like the typical ones, but just change the `submission_template` to point to the new containerized templates described in the previous section, and then they add the `singularity_args` variable, which is what will populate the `{SINGULARITY_ARGS}` variable in the template. Here we've used these to bind (mount) particular file systems the container will need. You can use these to pass along any environment-specific settings to your singularity container.

With this setup, if you want to run a singularity container, just specify `--compute singularity_slurm` or `--compute singularity_local` and it will use the appropriate template. 

For another example, take a look at the basic `localhost_container.yaml` PEPENV file, which describes a possible setup for running docker on a local computer:

```
compute:
  default:
    submission_template: templates/localhost_template.sub
    submission_command: sh
  singularity:
    submission_template: templates/localhost_singularity_template.sub
    submission_command: sh
    singularity_args: --bind /ext:/ext
  docker:
    submission_template: templates/localhost_docker_template.sub
    submission_command: sh
    docker_args: |
      --user=$(id -u) \
      --env="DISPLAY" \
      --volume ${HOME}:${HOME} \
      --volume="/etc/group:/etc/group:ro" \
      --volume="/etc/passwd:/etc/passwd:ro" \
      --volume="/etc/shadow:/etc/shadow:ro"  \
      --volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
      --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
      --workdir="`pwd`" \
```

Notice the `--volume` arguments, which mount disk volumes from the host into the container. This should work out of the box for most docker users.
