
import logging
import os
import sys
import yaml

from .attribute_dict import AttributeDict

_LOGGER = logging.getLogger(__name__)

class ComputingConfiguration(AttributeDict):
	"""Representation of common computing configuration file"""

	def __init__(self, cfg):
		self.cfg = cfg

    def set_compute(self, setting):
        """
        Set the compute attributes according to the
        specified settings in the environment file.

        :param str setting:	name for non-resource compute bundle, the name of
            a subsection in an environment configuration file
        :return bool: success flag for attempt to establish compute settings
        """

        # Hope that environment & environment compute are present.
        if setting and self.environment and "compute" in self.environment:
            # Augment compute, creating it if needed.
            if self.compute is None:
                _LOGGER.debug("Creating Project compute")
                self.compute = AttributeDict()
                _LOGGER.debug("Adding entries for setting '%s'", setting)
            self.compute.add_entries(self.environment.compute[setting])

            # Ensure submission template is absolute.
            if not os.path.isabs(self.compute.submission_template):
                try:
                    self.compute.submission_template = os.path.join(
                        os.path.dirname(self.environment_file),
                        self.compute.submission_template)
                except AttributeError as e:
                    # Environment and environment compute should at least have been
                    # set as null-valued attributes, so execution here is an error.
                    _LOGGER.error(str(e))
                    # Compute settings have been established.
                else:
                    return True
        else:
            # Scenario in which environment and environment compute are
            # both present--but don't evaluate to True--is fairly harmless.
            _LOGGER.debug("Environment = {}".format(self.environment))

        return False


    def update_environment(self, env_settings_file):
        """
        Parse data from environment configuration file.

        :param str env_settings_file: path to file with
            new environment configuration data
        """

        with open(env_settings_file, 'r') as f:
            _LOGGER.info("Loading %s: %s",
                         self.compute_env_var, env_settings_file)
            env_settings = yaml.load(f)
            _LOGGER.debug("Parsed environment settings: %s",
                          str(env_settings))

            # Any compute.submission_template variables should be made
            # absolute, relative to current environment settings file.
            y = env_settings["compute"]
            for key, value in y.items():
                if type(y[key]) is dict:
                    for key2, value2 in y[key].items():
                        if key2 == "submission_template":
                            if not os.path.isabs(y[key][key2]):
                                y[key][key2] = os.path.join(
                                    os.path.dirname(env_settings_file),
                                    y[key][key2])

            env_settings["compute"] = y
            if self.environment is None:
                self.environment = AttributeDict(env_settings)
            else:
                self.environment.add_entries(env_settings)

        self.environment_file = env_settings_file
