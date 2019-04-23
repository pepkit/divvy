""" Computing configuration representation """

import argparse
import logging
import os
import sys
import yaml
from yaml import SafeLoader

from attmap import PathExAttMap
from .const import COMPUTE_SETTINGS_VARNAME, DEFAULT_COMPUTE_RESOURCES_NAME, \
    NEW_COMPUTE_KEY
from .utils import parse_config_file, write_submit_script, get_first_env_var
from . import __version__

_LOGGER = logging.getLogger(__name__)


class ComputingConfiguration(PathExAttMap):
    """
    Represents computing configuration objects.

    The ComputingConfiguration class provides a computing configuration object
    that is an *in memory* representation of a `divvy` computing configuration
    file. This object has various functions to allow a user to activate, modify,
    and retrieve computing configuration files, and use these values to populate
    job submission script templates.
    
    :param str config_file: YAML file specifying computing package data (The
        `DIVCFG` file).
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
            _LOGGER.debug("No local config file was provided")
            _LOGGER.debug("Checking this set of environment variables: {}".format(self.compute_env_var))
            divcfg_env_var, divcfg_file = get_first_env_var(self.compute_env_var) or ["", ""]
            if os.path.isfile(divcfg_file):
                _LOGGER.debug("Found global config file in {}: {}".
                             format(divcfg_env_var, divcfg_file))
                self.config_file = divcfg_file
            else:
                _LOGGER.info("Using default config file, no global config file provided in environment "
                             "variable(s): {}".format(str(self.compute_env_var)))
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

        :return list[str]: names of candidate environment variables, for which
            value may be path to compute settings file; first found is used.
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
        Activates a compute package.

        This copies the computing attributes from the configuration file into
        the `compute` attribute, where the class stores current compute
        settings.

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
                self.compute = PathExAttMap()
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
        Clear current active settings and then activate the given package.

        :param str package_name: name of the resource package to activate
        :return bool: success flag
        """
        self.reset_active_settings()
        return self.activate_package(package_name)

    def get_active_package(self):
        """
        Returns settings for the currently active compute package

        :return PathExAttMap: data defining the active compute package
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
        self.compute = PathExAttMap()
        return True

    def update_packages(self, config_file):
        """
        Parse data from divvy configuration file.

        Given a divvy configuration file, this function will update (not
        overwrite) existing compute packages with existing values. It does not
        affect any currently active settings.
        
        :param str config_file: path to file with new divvy configuration data
        """
        env_settings = parse_config_file(config_file)
        loaded_packages = env_settings[NEW_COMPUTE_KEY]
        for key, value in loaded_packages.items():
            if type(loaded_packages[key]) is dict:
                for key2, value2 in loaded_packages[key].items():
                    if key2 == "submission_template":
                        if not os.path.isabs(loaded_packages[key][key2]):
                            loaded_packages[key][key2] = os.path.join(
                                os.path.dirname(config_file),
                                loaded_packages[key][key2])

        if self.compute_packages is None:
            self.compute_packages = PathExAttMap(loaded_packages)
        else:
            self.compute_packages.add_entries(loaded_packages)

        _LOGGER.debug("Available divvy packages: {}".
                      format(', '.join(self.list_compute_packages())))
        self.config_file = config_file

    def write_script(self, output_path, extra_vars=None):
        """
        Given currently active settings, populate the active template to write a
         submission script.

        :param str output_path: Path to file to write as submission script
        :param Iterable[Mapping] extra_vars: A list of Dict objects with key-value pairs
            with which to populate template fields. These will override any
            values in the currently active compute package.
        :return str: Path to the submission script file
        """
        from copy import deepcopy
        variables = deepcopy(self.compute)
        if extra_vars:
            if not isinstance(extra_vars, list):
                extra_vars = [extra_vars]
            for kvs in reversed(extra_vars):
                variables.update(kvs)
        _LOGGER.info("Writing script to {}".format(os.path.abspath(output_path)))
        return write_submit_script(output_path, self.template, variables)

    def _handle_missing_env_attrs(self, config_file, when_missing):
        """ Default environment settings aren't required; warn, though. """
        missing_env_attrs = \
            [attr for attr in [NEW_COMPUTE_KEY, "config_file"]
             if getattr(self, attr, None) is None]
        if not missing_env_attrs:
            return
        message = "'{}' lacks environment attributes: {}". \
            format(config_file, missing_env_attrs)
        if when_missing is None:
            _LOGGER.warning(message)
        else:
            when_missing(message)


class _VersionInHelpParser(argparse.ArgumentParser):
    def format_help(self):
        """ Add version information to help text. """
        return "version: {}\n".format(__version__) + \
               super(_VersionInHelpParser, self).format_help()


def main():
    """ Primary workflow """

    banner = "%(prog)s - write compute job scripts that can be submitted to any computing resource"
    additional_description = "\nhttps://github.com/pepkit/divvy"

    parser = _VersionInHelpParser(
            description=banner,
            epilog=additional_description)

    parser.add_argument(
            "-V", "--version",
            action="version",
            version="%(prog)s {v}".format(v=__version__))

    parser.add_argument(
            "-C", "--config",
            help="Divvy configuration file.")

    subparsers = parser.add_subparsers(dest="command") 


    def add_subparser(cmd):
        # Individual subcommands
        msg_by_cmd = {
            "list": "List available compute packages",
            "write": "Write a submit script"
        }
        return subparsers.add_parser(
            cmd, description=msg_by_cmd[cmd], help=msg_by_cmd[cmd])

    write_subparser = add_subparser("write")

    write_subparser.add_argument(
            "-S", "--settings",
            help="YAML file with job settings to populate the template.")    

    write_subparser.add_argument(
            "-P", "--package", default=DEFAULT_COMPUTE_RESOURCES_NAME,
            help="Compute package")

    write_subparser.add_argument(
            "-O", "--outfile", required=True,
            help="Output filepath")

    args, remaining_args = parser.parse_known_args()
    keys = [str.replace(x, "--", "") for x in remaining_args[::2]]
    cli_vars = dict(zip(keys, remaining_args[1::2]))
    dcc = ComputingConfiguration(args.config)

    if args.command == "list":
        print("Available compute packages:\n{}".format(
            "\n".join(dcc.list_compute_packages())))
        sys.exit(1)

    dcc.activate_package(args.package)
    if args.settings:
        _LOGGER.info("Loading settings file: %s", args.settings)
        with open(args.settings, 'r') as f:
            vars_groups = [cli_vars, yaml.load(f, SafeLoader)]
    else:
        vars_groups = [cli_vars]
    dcc.write_script(args.outfile, vars_groups)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        _LOGGER.error("Program canceled by user!")
        sys.exit(1)
