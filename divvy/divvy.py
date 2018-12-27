
import logging
import os
import sys
import yaml

from .attribute_dict import AttributeDict

from .const import \
    COMPUTE_SETTINGS_VARNAME, \
    DEFAULT_COMPUTE_RESOURCES_NAME

_LOGGER = logging.getLogger(__name__)

class ComputingConfiguration(AttributeDict):
    """Representation of common computing configuration file"""

    def __init__(self, cfg, default_compute=None, compute_env_file=None,
                 no_environment_exception=None, no_compute_exception=None):
        self.cfg = cfg
        self.environment, self.environment_file = None, None

        try:
            self.update_environment(
                default_compute or self.default_compute_envfile)
        except Exception as e:
            _LOGGER.error("Can't load environment config file '%s'",
                          str(default_compute))
            _LOGGER.error(str(type(e).__name__) + str(e))

        self._handle_missing_env_attrs(
            default_compute, when_missing=no_environment_exception)

        # Load settings from environment yaml for local compute infrastructure.
        compute_env_file = compute_env_file or os.getenv(self.compute_env_var)
        if compute_env_file:
            if os.path.isfile(compute_env_file):
                self.update_environment(compute_env_file)
            else:
                _LOGGER.warning("Compute env path isn't a file: {}".
                             format(compute_env_file))
        else:
            _LOGGER.info("No compute env file was provided and {} is unset; "
                         "using default".format(self.compute_env_var))

        # Initialize default compute settings.
        _LOGGER.debug("Establishing project compute settings")
        self.compute = None
        self.set_compute(DEFAULT_COMPUTE_RESOURCES_NAME)

        # Either warn or raise exception if the compute is null.
        if self.compute is None:
            message = "Failed to establish project compute settings"
            if no_compute_exception:
                no_compute_exception(message)
            else:
                _LOGGER.warning(message)
        else:
            _LOGGER.debug("Compute: %s", str(self.compute))



    def set_compute(self, setting):
        """
        Set the compute attributes according to the
        specified settings in the environment file.

        :param str setting: name for non-resource compute bundle, the name of
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


    def _handle_missing_env_attrs(self, env_settings_file, when_missing):
        """ Default environment settings aren't required; warn, though. """
        missing_env_attrs = \
            [attr for attr in ["environment", "environment_file"]
             if not hasattr(self, attr) or getattr(self, attr) is None]
        if not missing_env_attrs:
            return
        message = "'{}' lacks environment attributes: {}". \
            format(env_settings_file, missing_env_attrs)
        if when_missing is None:
            _LOGGER.warning(message)
        else:
            when_missing(message)


    @property
    def compute_env_var(self):
        """
        Environment variable through which to access compute settings.

        :return str: name of the environment variable to pointing to
            compute settings
        """
        return COMPUTE_SETTINGS_VARNAME


    @property
    def default_compute_envfile(self):
        """ Path to default compute environment settings file. """
        return os.path.join(
            self.templates_folder, "default_compute_settings.yaml")

