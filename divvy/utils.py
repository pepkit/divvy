""" Helpers without an obvious logical home. """

import logging
import os
import re


_LOGGER = logging.getLogger(__name__)


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

    keys_left = re.findall(r"!$\{(.+?)\}", content)
    if len(keys_left) > 0:
        _LOGGER.warning(
            "> Warning: %d submission template variables are not " "populated: '%s'",
            len(keys_left),
            str(keys_left),
        )

    if not fp:
        print(content)
        return content
    else:
        outdir = os.path.dirname(fp)
        if outdir and not os.path.isdir(outdir):
            os.makedirs(outdir)
        with open(fp, "w") as f:
            f.write(content)
        return fp
