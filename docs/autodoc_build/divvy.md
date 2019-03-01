# Package divvy Documentation

## Class ComputingConfiguration
Represents computing configuration objects.

The ComputingConfiguration class provides a computing configuration object
that is an *in memory* representation of a `divvy` computing configuration
file. This object has various functions to allow a user to activate, modify,
and retrieve computing configuration files, and use these values to populate
job submission script templates.

**Parameters:**

- `config_file` -- `str`:  YAML file specifying computing package data (The`DIVCFG` file).
- `no_env_error` -- `type`:  type of exception to raise if divvysettings can't be established, optional; if null (the default), a warning message will be logged, and no exception will be raised.
- `no_compute_exception` -- `type`:  type of exception to raise if computesettings can't be established, optional; if null (the default), a warning message will be logged, and no exception will be raised.


### activate\_package
Activates a compute package.

This copies the computing attributes from the configuration file into
the `compute` attribute, where the class stores current compute
settings.
```python
def activate_package(self, package_name):
```

**Parameters:**

- `package_name` -- `str`:  name for non-resource compute bundle,the name of a subsection in an environment configuration file


**Returns:**

`bool`:  success flag for attempt to establish compute settings




### add\_entries
Update this instance with provided key-value pairs.
```python
def add_entries(self, entries):
```

**Parameters:**

- `entries` -- `Iterable[(object, object)] | Mapping | pandas.Series`: collection of pairs of keys and values




### clean\_start
Clear current active settings and then activate the given package.
```python
def clean_start(self, package_name):
```

**Parameters:**

- `package_name` -- `str`:  name of the resource package to activate


**Returns:**

`bool`:  success flag




### clear
D.clear() -> None.  Remove all items from D.
```python
def clear(self):
```




### compute\_env\_var
Environment variable through which to access compute settings.
```python
def compute_env_var:
```

**Returns:**

`str`:  name of the environment variable to pointing tocompute settings




### copy
Copy self to a new object.
```python
def copy(self):
```




### default\_config\_file
Path to default compute environment settings file.
```python
def default_config_file:
```

**Returns:**

`str`:  Path to default compute settings file




### get
D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.
```python
def get(self, key, default=None):
```




### get\_active\_package
Returns settings for the currently active compute package
```python
def get_active_package(self):
```

**Returns:**

`AttMap`:  data defining the active compute package




### is\_null
Conjunction of presence in underlying mapping and value being None
```python
def is_null(self, item):
```

**Parameters:**

- `item` -- `object`:  Key to check for presence and null value


**Returns:**

`bool`:  True iff the item is present and has null value




### items
D.items() -> list of D's (key, value) pairs, as 2-tuples
```python
def items(self):
```




### iteritems
D.iteritems() -> an iterator over the (key, value) items of D
```python
def iteritems(self):
```




### iterkeys
D.iterkeys() -> an iterator over the keys of D
```python
def iterkeys(self):
```




### itervalues
D.itervalues() -> an iterator over the values of D
```python
def itervalues(self):
```




### keys
D.keys() -> list of D's keys
```python
def keys(self):
```




### list\_compute\_packages
Returns a list of available compute packages.
```python
def list_compute_packages(self):
```

**Returns:**

`set[str]`:  names of available compute packages




### non\_null
Conjunction of presence in underlying mapping and value not being None
```python
def non_null(self, item):
```

**Parameters:**

- `item` -- `object`:  Key to check for presence and non-null value


**Returns:**

`bool`:  True iff the item is present and has non-null value




### pop
D.pop(k[,d]) -> v, remove specified key and return the corresponding value. If key is not found, d is returned if given, otherwise KeyError is raised.
```python
def pop(self, key, default=<object object at 0x7f449d6ef030>):
```




### popitem
D.popitem() -> (k, v), remove and return some (key, value) pair as a 2-tuple; but raise KeyError if D is empty.
```python
def popitem(self):
```




### reset\_active\_settings
Clear out current compute settings.
```python
def reset_active_settings(self):
```

**Returns:**

`bool`:  success flag




### setdefault
D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D
```python
def setdefault(self, key, default=None):
```




### template
Get the currently active submission template.
```python
def template:
```

**Returns:**

`str`:  submission script content template for current state




### templates\_folder
Path to folder with default submission templates.
```python
def templates_folder:
```

**Returns:**

`str`:  path to folder with default submission templates




### update
D.update([E, ]**F) -> None.  Update D from mapping/iterable E and F. If E present and has a .keys() method, does:     for k in E: D[k] = E[k] If E present and lacks .keys() method, does:     for (k, v) in E: D[k] = v In either case, this is followed by: for k, v in F.items(): D[k] = v
```python
def update(*args, **kwds):
```




### update\_packages
Parse data from divvy configuration file.

Given a divvy configuration file, this function will update (not
overwrite) existing compute packages with existing values. It does not
affect any currently active settings.
```python
def update_packages(self, config_file):
```

**Parameters:**

- `config_file` -- `str`:  path to file withnew divvy configuration data




### values
D.values() -> list of D's values
```python
def values(self):
```




### write\_script
Given currently active settings, populate the active template to write a submission script.
```python
def write_script(self, output_path, extra_vars=None):
```

**Parameters:**

- `output_path` -- `str`:  Path to file to write as submission script
- `extra_vars` -- `Mapping`:  A list of Dict objects with key-value pairswith which to populate template fields. These will override any values in the currently active compute package.


**Returns:**

`str`:  Path to the submission script file




### write\_submit\_script
Write a submission script by populating a template with data.
```python
def write_submit_script(fp, content, data):
```

**Parameters:**

- `fp` -- `str`:  Path to the file to which to create/write submissions script.
- `content` -- `str`:  Template for submission script, defining keys thatwill be filled by given data
- `data` -- `Mapping`:  a "pool" from which values are available to replacekeys in the template


**Returns:**

`str`:  Path to the submission script



