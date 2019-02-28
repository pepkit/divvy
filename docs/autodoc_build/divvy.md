# Package divvy Documentation

Project configuration, particularly for logging.

Project-scope constants may reside here, but more importantly, some setup here
will provide a logging infrastructure for all of the project's modules.
Individual modules and classes may provide separate configuration on a more
local level, but this will at least provide a foundation.


## Class ComputingConfiguration
Representation of divvy computing configuration file
Representation of divvy computing configuration file

**Parameters:**

- `config_file` -- `str`:  YAML file specifying computing package data
- `no_env_error` -- `type`:  type of exception to raise if divvysettings can't be established, optional; if null (the default), a warning message will be logged, and no exception will be raised.


### activate\_package
Set compute attributes according to settings in environment file.
```python
def activate_package(self, package_name):
```

**Parameters:**

- `package_name` -- `str`:  name for non-resource compute bundle,the name of a subsection in an environment configuration file




### add\_entries
Update this instance with provided key-value pairs.
```python
def add_entries(self, entries):
```




### clean\_start
Clear settings and then activate the given package.
```python
def clean_start(self, package_name):
```

**Parameters:**

- `package_name` -- `str`:  name of the resource package to activate




### clear
D.clear() -> None.  Remove all items from D.
```python
def clear(self):
```




### copy
Copy self to a new object.
```python
def copy(self):
```




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




### is\_null
Conjunction of presence in underlying mapping and value being None
```python
def is_null(self, item):
```

**Parameters:**

- `item` -- `object`:  Key to check for presence and null value




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




### non\_null
Conjunction of presence in underlying mapping and value not being None
```python
def non_null(self, item):
```

**Parameters:**

- `item` -- `object`:  Key to check for presence and non-null value




### pop
D.pop(k[,d]) -> v, remove specified key and return the corresponding value.

If key is not found, d is returned if given, otherwise KeyError is raised.
```python
def pop(self, key, default=<object object at 0x7f5d0764d030>):
```




### popitem
D.popitem() -> (k, v), remove and return some (key, value) pair

as a 2-tuple; but raise KeyError if D is empty.
```python
def popitem(self):
```




### reset\_active\_settings
Clear out current compute settings.
```python
def reset_active_settings(self):
```




### setdefault
D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D
```python
def setdefault(self, key, default=None):
```




### update
D.update([E, ]**F) -> None.  Update D from mapping/iterable E and F.

If E present and has a .keys() method, does:     for k in E: D[k] = E[k]
If E present and lacks .keys() method, does:     for (k, v) in E: D[k] = v
In either case, this is followed by: for k, v in F.items(): D[k] = v
```python
def update(*args, **kwds):
```




### update\_packages
Parse data from divvy configuration file.
```python
def update_packages(self, config_file):
```




### values
D.values() -> list of D's values
```python
def values(self):
```




### write\_script
Given currently active settings, write a job(s) submission script.
```python
def write_script(self, output_path, extra_vars=None):
```

**Parameters:**

- `output_path` -- `str`:  Path to file to write as submission script
- `extra_vars` -- `Mapping`:  A list of Dict objects with key-value pairswith which to populate template fields. These will override any values in the currently active compute package.



