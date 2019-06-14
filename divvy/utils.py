""" Helpers without an obvious logical home. """

import logging
import os
import re
import warnings
import yaml
from .const import NEW_COMPUTE_KEY, OLD_COMPUTE_KEY


_LOGGER = logging.getLogger(__name__)


def check_sample_sheet_row_count(sheet, filepath):
    """
    Quick-and-dirt proxy for Sample count validation.

    Check that that the number of rows in a DataFrame (representing the
    Sample annotations sheet) seems correct given the number of lines in
    the file from which it was parsed/built.

    :param pandas.core.frame.DataFrame sheet: the sample annotations sheet
    :param str filepath: the path from which the sheet was built
    :return bool: flag indicating whether Sample (row) count seems correct
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()
    # Always deduct 1 line for header; accommodate final whitespace line.
    deduction = 2 if "" == lines[-1].strip() else 1
    return len(sheet) == len(lines) - deduction


def copy(obj):
    def copy(self):
        """
        Copy self to a new object.
        """
        from copy import deepcopy

        return deepcopy(self)
    obj.copy = copy
    return obj


def parse_config_file(conf_file):
    """
    Parse a divvy configuration file.

    :param str conf_file: path to divvy configuration file
    :return Mapping: compute settings as declared in config file
    """
    with open(conf_file, 'r') as f:
        _LOGGER.info("Loading divvy config file: %s", conf_file)
        env_settings = yaml.load(f, yaml.SafeLoader)
    _LOGGER.debug("Parsed environment settings: %s",
                  str(env_settings))
    # Any compute.submission_template variables should be made
    # absolute, relative to current divvy configuration file.
    if OLD_COMPUTE_KEY in env_settings:
        warnings.warn("Divvy compute configuration '{}' section changed "
                      "to '{}'".format(OLD_COMPUTE_KEY, NEW_COMPUTE_KEY),
                      DeprecationWarning)
        env_settings[NEW_COMPUTE_KEY] = env_settings[OLD_COMPUTE_KEY]
    return env_settings



def write_submit_script(fp, content, data):
    """
    Write a submission script by populating a template with data.

    :param str fp: Path to the file to which to create/write submissions script.
    :param str content: Template for submission script, defining keys that 
        will be filled by given data
    :param Mapping data: a "pool" from which values are available to replace 
        keys in the template
    :return str: Path to the submission script
    """

    for k, v in data.items():
        placeholder = "{" + str(k).upper() + "}"
        content = content.replace(placeholder, str(v))

    keys_left = re.findall(r'!$\{(.+?)\}', content)
    if len(keys_left) > 0:
        _LOGGER.warning("> Warning: %d submission template variables are not "
                        "populated: '%s'", len(keys_left), str(keys_left))

    outdir = os.path.dirname(fp)
    if outdir and not os.path.isdir(outdir):
        os.makedirs(outdir)
    with open(fp, 'w') as f:
        f.write(content)
    return fp


def get_first_env_var(ev):
    """
    Get the name and value of the first set environment variable

    :param ev: a list of the environment variable names
    :type: list[str] | str
    :return: name and the value of the environment variable
    :rtype: list
    """
    if not isinstance(ev, list):
        if isinstance(ev, str):
            ev = [ev]
        else:
            raise TypeError("The argument has to be a list or string.")
    for i in ev:
        if os.getenv(i, False):
            return [i, os.getenv(i)]
