""" Package constants """

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


# Compute-related
COMPUTE_SETTINGS_VARNAME = ["DIVCFG", "PEPENV"]
DEFAULT_COMPUTE_RESOURCES_NAME = "default"
OLD_COMPUTE_KEY = "compute"
NEW_COMPUTE_KEY = "compute_packages"
COMPUTE_CONSTANTS = [
    "COMPUTE_SETTINGS_VARNAME", "DEFAULT_COMPUTE_RESOURCES_NAME",
    "NEW_COMPUTE_KEY"]

__all__ = COMPUTE_CONSTANTS + ["DEFAULT_COMPUTE_RESOURCES_NAME"]
