""" Computing configuration representation """


import argparse
import logging
import logmuse
import os
import sys
import shutil
import yaml
from yaml import SafeLoader
from distutils.dir_util import copy_tree

# from attmap import PathExAttMap
from ubiquerg import is_writable
import yacman
from collections import OrderedDict

from .const import COMPUTE_SETTINGS_VARNAME, DEFAULT_COMPUTE_RESOURCES_NAME, \
    NEW_COMPUTE_KEY
from .utils import parse_config_file, write_submit_script, get_first_env_var
from . import __version__

DEFAULT_CONFIG_FILEPATH = os.path.join(
        os.path.dirname(__file__),
        "default_config",
        "divvy_config.yaml")

_LOGGER = logging.getLogger(__name__)


class ComputingConfiguration(yacman.YacAttMap):
    """
    Represents computing configuration objects.

    The ComputingConfiguration class provides a computing configuration object
    that is an *in memory* representation of a `divvy` computing configuration
    file. This object has various functions to allow a user to activate, modify,
    and retrieve computing configuration files, and use these values to populate
    job submission script templates.
    
    :param str | Iterable[(str, object)] | Mapping[str, object] entries: config
        Collection of key-value pairs.
    :param str filepath: YAML file specifying computing package data. (the
        `DIVCFG` file)
    """

    def __init__(self, entries=None, filepath=None, 
                config_file=None,  # for backwards compatibility with peppy 0.22
                no_env_error=None,  # for backwards compatibility with peppy 0.22
                no_compute_exception=None): # for backwards compatibility with peppy 0.22

        if no_env_error:
            _LOGGER.debug("The no_env_error argument has been deprecated. It will be removed in the next version of divvy")

        if no_compute_exception:
            _LOGGER.debug("The no_compute_exception argument has been deprecated. It will be removed in the next version of divvy")

        if config_file:  # for backwards compatibility with peppy 0.22 (remove later)
            _LOGGER.debug("The config_file argument has renamed filepath.")
            filepath = select_divvy_config(config_file)

        if not entries and not filepath and not config_file:
            # Handle the case of an empty one, when we'll use the default
            filepath = select_divvy_config(None)

        super(ComputingConfiguration, self).__init__(entries, filepath)

        if not hasattr(self, "compute_packages"):
            raise Exception("Your divvy config file is not in divvy config format (it"
            " lacks a compute_packages section): '{}'".format(filepath))
            # We require that compute_packages be present, even if empty
            self.compute_packages = {}

        # Initialize default compute settings.
        _LOGGER.debug("Establishing project compute settings")
        self.compute = None
        self.activate_package(DEFAULT_COMPUTE_RESOURCES_NAME)
        self.config_file = self._file_path

    def write(self, filename=None):
        super(ComputingConfiguration, self).write(filename)
        filename = filename or getattr(self, yacman.FILEPATH_KEY)
        filedir = os.path.dirname(filename)
        # For this object, we *also* have to write the template files
        for pkg_name, pkg in self.compute_packages.items():
            print(pkg)
            destfile = os.path.join(filedir, os.path.basename(pkg.submission_template))
            shutil.copyfile(pkg.submission_template, destfile)

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
        return DEFAULT_CONFIG_FILEPATH

    # Warning: template cannot be a property, because otherwise
    # it will get treated as a PathExAttMap treats all properties, which
    # is that it will turn any double-slashes into single slashes.
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
        return os.path.join(os.path.dirname(__file__), "default_config", "submit_templates")

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
        act_msg = "Activating compute package '{}'".format(package_name)
        if package_name == "default":
            _LOGGER.debug(act_msg)
        else:
            _LOGGER.info(act_msg)

        if package_name and self.compute_packages and package_name in self.compute_packages:
            # Augment compute, creating it if needed.
            if self.compute is None:
                _LOGGER.debug("Creating Project compute")
                self.compute = yacman.YacAttMap()
                _LOGGER.debug("Adding entries for package_name '%s'", package_name)

            self.compute.add_entries(self.compute_packages[package_name])

            # Ensure submission template is absolute. This *used to be* handled
            # at update (so the paths were stored as absolutes in the packages),
            # but now, it makes more sense to do it here so we can piggyback on
            # the default update() method and not even have to do that.
            if not os.path.isabs(self.compute.submission_template):
                try:
                    self.compute.submission_template = os.path.join(
                        os.path.dirname(self._file_path),
                        self.compute.submission_template)
                except AttributeError as e:
                    # Environment and environment compute should at least have been
                    # set as null-valued attributes, so execution here is an error.
                    _LOGGER.error(str(e))

            _LOGGER.debug("Submit template set to: {}".format(self.compute.submission_template))
            # _LOGGER.debug("Submit template set to: {}".format(self["compute"]["submission_template"]))

            return True

        else:
            # Scenario in which environment and environment compute are
            # both present--but don't evaluate to True--is fairly harmless.
            _LOGGER.debug("Can't activate package. compute_packages = {}".format(self.compute_packages))

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

        :return yacman.YacAttMap: data defining the active compute package
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
        self.compute = yacman.YacAttMap()
        return True

    def update_packages(self, config_file):
        """
        Parse data from divvy configuration file.

        Given a divvy configuration file, this function will update (not
        overwrite) existing compute packages with existing values. It does not
        affect any currently active settings.
        
        :param str config_file: path to file with new divvy configuration data
        """
        entries = yacman.load_yaml(config_file)
        self.update(entries)
        return True

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
        _LOGGER.debug("Submission template: {}".format(self.compute.submission_template))
        return write_submit_script(output_path, self.template(), variables)

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


def select_divvy_config(filepath):
    divcfg = yacman.select_config(
        filepath,
        COMPUTE_SETTINGS_VARNAME,
        default_config_filepath=DEFAULT_CONFIG_FILEPATH,
        check_exist=True)
    _LOGGER.debug("Selected divvy config: {}".format(divcfg))
    return divcfg


class _VersionInHelpParser(argparse.ArgumentParser):
    def format_help(self):
        """ Add version information to help text. """
        return "version: {}\n".format(__version__) + \
               super(_VersionInHelpParser, self).format_help()


def divvy_init(config_path, template_config_path):
    """
    Initialize a genome config file.
    
    :param str config_path: path to divvy configuration file to 
        create/initialize
    :param str template_config_path: path to divvy configuration file to 
        copy FROM
    """
    if not config_path:
        _LOGGER.error("You must specify a file path to initialize.")
        return

    if not template_config_path:
        _LOGGER.error("You must specify a template config file path.")
        return

    if config_path and not os.path.exists(config_path):
        # dcc.write(config_path)
        # Init should *also* write the templates.
        dest_folder = os.path.dirname(config_path)
        copy_tree(os.path.dirname(template_config_path), dest_folder)
        new_template = os.path.join(os.path.dirname(config_path), os.path.basename(template_config_path))
        os.rename(new_template, config_path)
        _LOGGER.info("Wrote new divvy configuration file: {}".format(config_path))
    else:
        _LOGGER.warning("Can't initialize, file exists: {} ".format(config_path))


def build_argparser():
    """
    Builds argument parser.

    :return argparse.ArgumentParser
    """

    banner = "%(prog)s - write compute job scripts that can be submitted to any computing resource"
    additional_description = "\nhttps://divvy.databio.org"

    parser = _VersionInHelpParser(
            prog="divvy",
            description=banner,
            epilog=additional_description)

    parser.add_argument(
            "-V", "--version",
            action="version",
            version="%(prog)s {v}".format(v=__version__))

    subparsers = parser.add_subparsers(dest="command") 

    def add_subparser(cmd, description):
        return subparsers.add_parser(
            cmd, description=description, help=description)

    subparser_messages = {
        "init": "Initialize a new divvy config file",
        "list": "List available compute packages",
        "write": "Write a job script"
    }

    sps = {}
    for cmd, desc in subparser_messages.items():
        sps[cmd] = add_subparser(cmd, desc)
        sps[cmd].add_argument(
            "-c", "--config", required=(cmd == "init"),
            help="Divvy configuration file.")

    sps["write"].add_argument(
            "-s", "--settings",
            help="YAML file with job settings to populate the template.")    

    sps["write"].add_argument(
            "-p", "--package", default=DEFAULT_COMPUTE_RESOURCES_NAME,
            help="Select from available compute packages.")

    # sps["write"].add_argument(
    #         "-t", "--template",
    #         help="Provide a template file (not yet implemented).")

    sps["write"].add_argument(
            "-o", "--outfile", required=True,
            help="Output filepath")

    return parser


def main():
    """ Primary workflow """

    parser = logmuse.add_logging_options(build_argparser())
    args, remaining_args = parser.parse_known_args()
    logger_kwargs = {"level": args.verbosity, "devmode": args.logdev}
    logmuse.init_logger(name="yacman", **logger_kwargs)
    global _LOGGER
    _LOGGER = logmuse.logger_via_cli(args)

    if not args.command:
        parser.print_help()
        _LOGGER.error("No command given")
        sys.exit(1)
    # Any non-divvy arguments will be passed along as key-value pairs
    # that can be used to populate the template.
    keys = [str.replace(x, "--", "") for x in remaining_args[::2]]
    cli_vars = dict(zip(keys, remaining_args[1::2]))

    if args.command == "init":
        divcfg = args.config
        _LOGGER.debug("Initializing divvy configuration")
        is_writable(os.path.dirname(divcfg), check_exist=False)
        divvy_init(divcfg, DEFAULT_CONFIG_FILEPATH)
        sys.exit(0)      

    divcfg = select_divvy_config(args.config)
    _LOGGER.info("Using divvy config: {}".format(divcfg))
    dcc = ComputingConfiguration(filepath=divcfg)

    if args.command == "list":
        # Output header via logger and content via print so the user can
        # redirect the list from stdout if desired without the header as clutter
        _LOGGER.info("Available compute packages:\n")
        print("{}".format("\n".join(dcc.list_compute_packages())))
        sys.exit(1)


    try:
        dcc.activate_package(args.package)
    except AttributeError:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.settings:
        _LOGGER.info("Loading settings file: %s", args.settings)
        with open(args.settings, 'r') as f:
            vars_groups = [cli_vars, yaml.load(f, SafeLoader)]
    else:
        vars_groups = [cli_vars]
    dcc.write_script(args.outfile, vars_groups)
