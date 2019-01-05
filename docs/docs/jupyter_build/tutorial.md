
# Example of how to use Divvy

Start by importing `divvy`, and then let's create a new `ComputingConfiguration` object with no arguments:


```python
import divvy
```


```python
dcc = divvy.ComputingConfiguration()
```

    No local config file was provided
    No global config file was provided in environment variable DIVCFG
    Using default config file.
    Loading divvy config file: /home/nsheff/.local/lib/python2.7/site-packages/divvy/submit_templates/default_compute_settings.yaml
    Available packages: ['default', 'local', 'slurm']
    Activating compute package 'default'


Now we see that there are a few compute packages available, and the 'default' package has been automatically activated. We can explore the compute settings in this package like this: 


```python
dcc.compute
```




    {'submission_command': 'sh', 'submission_template': '/home/nsheff/.local/lib/python2.7/site-packages/divvy/submit_templates/localhost_template.sub'}



And we can activate a different one like this: 


```python
dcc.activate_package("slurm")
```

    Activating compute package 'slurm'





    True



It returns 'True' to indicate that the activation has been successful. This will change our settings:


```python
dcc.compute
```




    {'submission_command': 'sbatch', 'example_variable': 'blah', 'submission_template': '/home/nsheff/.local/lib/python2.7/site-packages/divvy/submit_templates/slurm_template.sub'}


