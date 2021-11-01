""" Package constants """
import os

# Compute-related
COMPUTE_SETTINGS_VARNAME = ["DIVCFG"]
DEFAULT_COMPUTE_RESOURCES_NAME = "default"
OLD_COMPUTE_KEY = "compute"
NEW_COMPUTE_KEY = "compute_packages"
DEFAULT_CONFIG_FILEPATH = os.path.join(
    os.path.dirname(__file__), "default_config", "divvy_config.yaml"
)
DEFAULT_CONFIG_SCHEMA = os.path.join(
    os.path.dirname(__file__), "schemas", "divvy_config_schema.yaml"
)
COMPUTE_CONSTANTS = [
    "COMPUTE_SETTINGS_VARNAME",
    "DEFAULT_COMPUTE_RESOURCES_NAME",
    "NEW_COMPUTE_KEY",
    "DEFAULT_CONFIG_FILEPATH",
    "DEFAULT_CONFIG_SCHEMA",
]

__all__ = COMPUTE_CONSTANTS + ["DEFAULT_COMPUTE_RESOURCES_NAME"]
