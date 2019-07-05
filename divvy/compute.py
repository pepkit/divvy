""" Computing configuration representation """


import argparse
import logging
import logmuse
import os
import sys
import shutil
import yaml
from yaml import SafeLoader

# from attmap import PathExAttMap
import yacman
from collections import OrderedDict

from .const import COMPUTE_SETTINGS_VARNAME, DEFAULT_COMPUTE_RESOURCES_NAME, \
    NEW_COMPUTE_KEY
from .utils import parse_config_file, write_submit_script, get_first_env_var
from . import __version__

_LOGGER = None
# _LOGGER = logging.getLogger(__name__)


class ComputingConfiguration(yacman.YacAttMap):
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

    def __init__(self, entries=None,
                 no_env_error=None, no_compute_exception=None):
        super(ComputingConfiguration, self).__init__(entries)

        self.compute_packages = None

        if entries:
             self.config_file = entries

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

    def write(self, filename=None):
        super(ComputingConfiguration, self).write(filename)
        filename = filename or getattr(self, FILEPATH_KEY)
        filedir = os.path.dirname(filename)
        # For this object, we *also* have to write the template files
        for pkg_name, pkg in self.compute_packages.items():
            print(pkg)
            destfile = os.path.join(filedir, os.path.basename(pkg.submission_template))
            copyfile(pkg.submission_template, destfile)

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
            self.compute_packages = yacman.YacAttMap(loaded_packages)
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


def divvy_init(config_path, template_config_path):
    """
    Initialize a genome config file.
    
    :param str config_path: path to genome configuration file to 
        create/initialize
    :param st genome_server: URL for a server
    """

    # Set up default 
    dcc = ComputingConfiguration(template_config_path)

    _LOGGER.debug("DCC: {}".format(dcc))

    if config_path and not os.path.exists(config_path):
        # dcc.write(config_path)
        # Init should *also* write the templates.
        shutil.copytree(os.path.dirname(template_config_path),os.path.dirname(config_path))
        new_template = os.path.join(os.path.dirname(config_path), os.path.basename(template_config_path))
        os.rename(new_template, config_path)
        _LOGGER.info("Wrote new divvy configuration file: {}".format(config_path))
    else:
        _LOGGER.warning("Can't initialize, file exists: {} ".format(config_path))

def _single_folder_writeable(d):
    return os.access(d, os.W_OK) and os.access(d, os.X_OK)

def _writeable(outdir, strict_exists=False):
    outdir = outdir or "."
    if os.path.exists(outdir):
        return _single_folder_writeable(outdir)
    elif strict_exists:
        raise MissingFolderError(outdir)
    return _writeable(os.path.dirname(outdir), strict_exists)


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
            "-c", "--config",
            help="Divvy configuration file.")

    subparsers = parser.add_subparsers(dest="command") 

    def add_subparser(cmd, description):
        return subparsers.add_parser(
            cmd, description=description, help=description)

    write_subparser = add_subparser("write", "Write a submit script")
    list_subparser = add_subparser("list", "List available compute packages")
    init_subparser = add_subparser("init", "Initialize a new divvy config file")

    write_subparser.add_argument(
            "-s", "--settings",
            help="YAML file with job settings to populate the template.")    

    write_subparser.add_argument(
            "-p", "--package", default=DEFAULT_COMPUTE_RESOURCES_NAME,
            help="Select from available compute packages.")

    # write_subparser.add_argument(
    #         "-t", "--template",
    #         help="Provide a template file (not yet implemented).")

    write_subparser.add_argument(
            "-o", "--outfile", required=True,
            help="Output filepath")

    parser = logmuse.add_logging_options(parser)
    args, remaining_args = parser.parse_known_args()
    global _LOGGER
    _LOGGER = logmuse.logger_via_cli(args)

    # Any non-divvy arguments will be passed along as key-value pairs
    # that can be used to populate the template.
    keys = [str.replace(x, "--", "") for x in remaining_args[::2]]
    cli_vars = dict(zip(keys, remaining_args[1::2]))

    default_config_filepath = os.path.join(
        os.path.dirname(__file__),
        "submit_templates",
        "default_compute_settings.yaml")

    divcfg = yacman.select_config(
        args.config, COMPUTE_SETTINGS_VARNAME,
        check_exist=not args.command == "init",  on_missing=lambda fp: fp,
        default_config_filepath=default_config_filepath)

    if args.command == "init":
        _LOGGER.debug("Initializing divvy configuration")
        _writeable(os.path.dirname(divcfg), strict_exists=False)
        divvy_init(divcfg, default_config_filepath)
        sys.exit(0)      


    _LOGGER.info("Divvy config: {}".format(divcfg))
    dcc = ComputingConfiguration(divcfg)

    if args.command == "list":
        print("Available compute packages:\n{}".format(
            "\n".join(dcc.list_compute_packages())))
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


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        _LOGGER.error("Program canceled by user!")
        sys.exit(1)
