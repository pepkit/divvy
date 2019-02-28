""" Computing configuration representation """

import logging
import os
import yaml

from attmap import AttMap
from .const import \
    COMPUTE_SETTINGS_VARNAME, \
    DEFAULT_COMPUTE_RESOURCES_NAME
from .utils import write_submit_script, get_first_env_var


_LOGGER = logging.getLogger(__name__)


class ComputingConfiguration(AttMap):
    """
    Representation of divvy computing configuration file
    
    :param str config_file: YAML file specifying computing package data
    :param type no_env_error: type of exception to raise if divvy
        settings can't be established, optional; if null (the default),
        a warning message will be logged, and no exception will be raised.
    :param type no_compute_exception: type of exception to raise if compute
        settings can't be established, optional; if null (the default),
        a warning message will be logged, and no exception will be raised.
    """

    def __init__(self, config_file=None,
                 no_env_error=None, no_compute_exception=None):

        super(ComputingConfiguration, self).__init__()

        self.compute_packages = None

        if config_file:
            if os.path.isfile(config_file):
                self.config_file = config_file
            else:
                _LOGGER.error("Config file path isn't a file: {}".
                              format(config_file))
                raise IOError(config_file)
        else:
            _LOGGER.info("No local config file was provided")
            _LOGGER.debug("Checking this set of environment variables: {}".format(self.compute_env_var))
            divcfg_env_var, divcfg_file = get_first_env_var(self.compute_env_var) or ["", ""]
            if os.path.isfile(divcfg_file):
                _LOGGER.info("Found global config file in {}: {}".
                             format(divcfg_env_var, divcfg_file))
                self.config_file = divcfg_file
            else:
                _LOGGER.info("No global config file was provided in environment "
                             "variable(s): {}".format(str(self.compute_env_var)))
                _LOGGER.info("Using default config file.")
                self.config_file = self.default_config_file

        try:
            self.update_packages(self.config_file)
        except Exception as e:
            _LOGGER.error("Can't load config file '%s'",
                          str(self.config_file))
            _LOGGER.error(str(type(e).__name__) + str(e))

        self._handle_missing_env_attrs(
            self.config_file, when_missing=no_env_error)

        # Initialize default compute settings.
        _LOGGER.debug("Establishing project compute settings")
        self.compute = None
        self.activate_package(DEFAULT_COMPUTE_RESOURCES_NAME)

        # Either warn or raise exception if the compute is null.
        if self.compute is None:
            message = "Failed to establish compute settings."
            if no_compute_exception:
                no_compute_exception(message)
            else:
                _LOGGER.warning(message)
        else:
            _LOGGER.debug("Compute: %s", str(self.compute))

    @property
    def compute_env_var(self):
        """
        Environment variable through which to access compute settings.
        :return str: name of the environment variable to pointing to
            compute settings
        """
        return COMPUTE_SETTINGS_VARNAME

    @property
    def default_config_file(self):
        """
        Path to default compute environment settings file.
        :return str: Path to default compute settings file
        """
        return os.path.join(
            self.templates_folder, "default_compute_settings.yaml")

    @property
    def template(self):
        """
        Get the currently active submission template.

        :return str: submission script content template for current state
        """
        with open(self.compute.submission_template, 'r') as f:
            return f.read()

    @property
    def templates_folder(self):
        """
        Path to folder with default submission templates.
        :return str: path to folder with default submission templates
        """
        return os.path.join(os.path.dirname(__file__), "submit_templates")

    def activate_package(self, package_name):
        """
        Set compute attributes according to settings in environment file.

        :param str package_name: name for non-resource compute bundle,
            the name of a subsection in an environment configuration file
        :return bool: success flag for attempt to establish compute settings
        """

        # Hope that environment & environment compute are present.
        _LOGGER.info("Activating compute package '{}'".format(package_name))

        if package_name and self.compute_packages and package_name in self.compute_packages:
            # Augment compute, creating it if needed.
            if self.compute is None:
                _LOGGER.debug("Creating Project compute")
                self.compute = AttMap()
                _LOGGER.debug("Adding entries for package_name '%s'", package_name)
            self.compute.add_entries(self.compute_packages[package_name])

            # Ensure submission template is absolute.
            # This is handled at update.
            # if not os.path.isabs(self.compute.submission_template):
            #     try:
            #         self.compute.submission_template = os.path.join(
            #             os.path.dirname(self.config_file),
            #             self.compute.submission_template)
            #     except AttributeError as e:
            #         # Environment and environment compute should at least have been
            #         # set as null-valued attributes, so execution here is an error.
            #         _LOGGER.error(str(e))

            return True

        else:
            # Scenario in which environment and environment compute are
            # both present--but don't evaluate to True--is fairly harmless.
            _LOGGER.debug("Environment = {}".format(self.compute_packages))

        return False

    def clean_start(self, package_name):
        """
        Clear settings and then activate the given package.

        :param str package_name: name of the resource package to activate
        :return bool: success flag
        """
        self.reset_active_settings()
        return self.activate_package(package_name)

    def get_active_package(self):
        """
        Returns settings for the currently active compute package
        :return AttMap: data defining the active compute package
        """
        return self.compute

    def list_compute_packages(self):
        """
        Returns a list of available compute packages.
        :return set[str]: names of available compute packages
        """
        return set(self.compute_packages.keys())

    def reset_active_settings(self):
        """
        Clear out current compute settings.
        :return bool: success flag
        """
        self.compute = AttMap()
        return True

    def update_packages(self, config_file):
        """
        Parse data from divvy configuration file.
        :param str config_file: path to file with
            new divvy configuration data
        """
        with open(config_file, 'r') as f:
            _LOGGER.info("Loading divvy config file: %s", config_file)
            env_settings = yaml.load(f)
            _LOGGER.debug("Parsed environment settings: %s",
                          str(env_settings))

            # Any compute.submission_template variables should be made
            # absolute, relative to current divvy configuration file.
            if "compute" in env_settings:
                _LOGGER.warn("Use 'compute_packages' instead of 'compute'")
                env_settings["compute_packages"] = env_settings["compute"]

            loaded_packages = env_settings["compute_packages"]
            for key, value in loaded_packages.items():
                if type(loaded_packages[key]) is dict:
                    for key2, value2 in loaded_packages[key].items():
                        if key2 == "submission_template":
                            if not os.path.isabs(loaded_packages[key][key2]):
                                loaded_packages[key][key2] = os.path.join(
                                    os.path.dirname(config_file),
                                    loaded_packages[key][key2])

            if self.compute_packages is None:
                self.compute_packages = AttMap(loaded_packages)
            else:
                self.compute_packages.add_entries(loaded_packages)
        _LOGGER.info("Available packages: {}".format(self.list_compute_packages()))
        self.config_file = config_file

    def write_script(self, output_path, extra_vars=None):
        """
        Given currently active settings, write a job(s) submission script.

        :param str output_path: Path to file to write as submission script
        :param Mapping extra_vars: A list of Dict objects with key-value pairs
            with which to populate template fields. These will override any
            values in the currently active compute package.
        :return str: Path to the submission script file
        """
        variables = self.compute
        if extra_vars:
            if not isinstance(extra_vars, list):
                extra_vars = [extra_vars]
            for item in extra_vars:
                variables.update(item)
        _LOGGER.info("Writing script to {}".format(os.path.abspath(output_path)))
        return write_submit_script(output_path, self.template, variables)

    def _handle_missing_env_attrs(self, config_file, when_missing):
        """ Default environment settings aren't required; warn, though. """
        missing_env_attrs = \
            [attr for attr in ["compute_packages", "config_file"]
             if not hasattr(self, attr) or getattr(self, attr) is None]
        if not missing_env_attrs:
            return
        message = "'{}' lacks environment attributes: {}". \
            format(config_file, missing_env_attrs)
        if when_missing is None:
            _LOGGER.warning(message)
        else:
            when_missing(message)
