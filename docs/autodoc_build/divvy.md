# Package divvy Documentation

Project configuration, particularly for logging.

Project-scope constants may reside here, but more importantly, some setup here
will provide a logging infrastructure for all of the project's modules.
Individual modules and classes may provide separate configuration on a more
local level, but this will at least provide a foundation.


## Class AttributeDict
A class to convert a nested mapping(s) into an object(s) with key-values
using object syntax (attr_dict.attribute) instead of getitem syntax
(attr_dict["key"]). This class recursively sets mappings to objects,
facilitating attribute traversal (e.g., attr_dict.attr.attr).
### \_\_init\_\_
```py

def __init__(self, entries=None, _force_nulls=False, _attribute_identity=False)

```



Establish a logger for this instance, set initial entries,
and determine behavior with regard to null values and behavior
for attribute requests.

:param collections.Iterable | collections.Mapping entries: collection
    of key-value pairs, initial data for this mapping
:param bool _force_nulls: whether to allow a null value to overwrite
    an existing non-null value
:param bool _attribute_identity: whether to return attribute name
    requested rather than exception when unset attribute/key is queried


### add\_entries
```py

def add_entries(self, entries)

```



Update this `AttributeDict` with provided key-value pairs.

:param Iterable[(object, object)] | Mapping | pandas.Series entries:
    collection of pairs of keys and values


### clear
```py

def clear(self)

```



D.clear() -> None.  Remove all items from D.


### copy
```py

def copy(self)

```



Copy self to a new object.


### get
```py

def get(self, key, default=None)

```



D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.


### is\_null
```py

def is_null(self, item)

```



Conjunction of presence in underlying mapping and value being None

:param object item: Key to check for presence and null value
:return bool: True iff the item is present and has null value


### items
```py

def items(self)

```



D.items() -> list of D's (key, value) pairs, as 2-tuples


### iteritems
```py

def iteritems(self)

```



D.iteritems() -> an iterator over the (key, value) items of D


### iterkeys
```py

def iterkeys(self)

```



D.iterkeys() -> an iterator over the keys of D


### itervalues
```py

def itervalues(self)

```



D.itervalues() -> an iterator over the values of D


### keys
```py

def keys(self)

```



D.keys() -> list of D's keys


### non\_null
```py

def non_null(self, item)

```



Conjunction of presence in underlying mapping and value not being None

:param object item: Key to check for presence and non-null value
:return bool: True iff the item is present and has non-null value


### pop
```py

def pop(self, key, default=<object object at 0x7f8e4253f030>)

```



D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
If key is not found, d is returned if given, otherwise KeyError is raised.


### popitem
```py

def popitem(self)

```



D.popitem() -> (k, v), remove and return some (key, value) pair
as a 2-tuple; but raise KeyError if D is empty.


### setdefault
```py

def setdefault(self, key, default=None)

```



D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D


### update
```py

def update(*args, **kwds)

```



D.update([E, ]**F) -> None.  Update D from mapping/iterable E and F.
If E present and has a .keys() method, does:     for k in E: D[k] = E[k]
If E present and lacks .keys() method, does:     for (k, v) in E: D[k] = v
In either case, this is followed by: for k, v in F.items(): D[k] = v


### values
```py

def values(self)

```



D.values() -> list of D's values




## Class ComputingConfiguration
Representation of divvy computing configuration file

:param str config_file: YAML file specifying computing package data
:param type no_env_error: type of exception to raise if environment 
    settings can't be established, optional; if null (the default), 
    a warning message will be logged, and no exception will be raised.
:param type no_compute_exception: type of exception to raise if compute
    settings can't be established, optional; if null (the default),
    a warning message will be logged, and no exception will be raised.
### \_\_init\_\_
```py

def __init__(self, config_file=None, no_env_error=None, no_compute_exception=None)

```



### activate\_package
```py

def activate_package(self, package_name)

```



Set the compute attributes according to the
specified settings in the environment file.

:param str package_name: name for non-resource compute bundle, the name of
    a subsection in an environment configuration file
:return bool: success flag for attempt to establish compute settings


### add\_entries
```py

def add_entries(self, entries)

```



Update this `AttributeDict` with provided key-value pairs.

:param Iterable[(object, object)] | Mapping | pandas.Series entries:
    collection of pairs of keys and values


### clean\_start
```py

def clean_start(self, package_name)

```



Clear settings and then activate the given package.


### clear
```py

def clear(self)

```



D.clear() -> None.  Remove all items from D.


### copy
```py

def copy(self)

```



Copy self to a new object.


### get
```py

def get(self, key, default=None)

```



D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.


### get\_active\_package
```py

def get_active_package(self)

```



Returns settings for the currently active compute package


### is\_null
```py

def is_null(self, item)

```



Conjunction of presence in underlying mapping and value being None

:param object item: Key to check for presence and null value
:return bool: True iff the item is present and has null value


### items
```py

def items(self)

```



D.items() -> list of D's (key, value) pairs, as 2-tuples


### iteritems
```py

def iteritems(self)

```



D.iteritems() -> an iterator over the (key, value) items of D


### iterkeys
```py

def iterkeys(self)

```



D.iterkeys() -> an iterator over the keys of D


### itervalues
```py

def itervalues(self)

```



D.itervalues() -> an iterator over the values of D


### keys
```py

def keys(self)

```



D.keys() -> list of D's keys


### list\_compute\_packages
```py

def list_compute_packages(self)

```



Returns a list of available compute packages.


### non\_null
```py

def non_null(self, item)

```



Conjunction of presence in underlying mapping and value not being None

:param object item: Key to check for presence and non-null value
:return bool: True iff the item is present and has non-null value


### pop
```py

def pop(self, key, default=<object object at 0x7f8e4253f030>)

```



D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
If key is not found, d is returned if given, otherwise KeyError is raised.


### popitem
```py

def popitem(self)

```



D.popitem() -> (k, v), remove and return some (key, value) pair
as a 2-tuple; but raise KeyError if D is empty.


### reset\_active\_settings
```py

def reset_active_settings(self)

```



Clear out current compute settings.


### setdefault
```py

def setdefault(self, key, default=None)

```



D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D


### update
```py

def update(*args, **kwds)

```



D.update([E, ]**F) -> None.  Update D from mapping/iterable E and F.
If E present and has a .keys() method, does:     for k in E: D[k] = E[k]
If E present and lacks .keys() method, does:     for (k, v) in E: D[k] = v
In either case, this is followed by: for k, v in F.items(): D[k] = v


### update\_packages
```py

def update_packages(self, config_file)

```



Parse data from environment configuration file.

:param str config_file: path to file with
    new environment configuration data


### values
```py

def values(self)

```



D.values() -> list of D's values




