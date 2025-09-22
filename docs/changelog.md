This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format. 

# Changelog

## [0.6.1] -- 2025-09-22
- Functionality has been moved to looper  https://github.com/pepkit/looper
- Repository is now archived

## [0.6.0] -- 2021-04-26

### Added
- divvy configuration file validation
- bulker localhost template default

### Fixed
- localhost commands to work with newline characters


## [0.5.0] -- 2020-05-19
### Added
- adapters support, see [#47](https://github.com/pepkit/divvy/issues/47) for detailed explanation
- `select_divvy_config` function
- `divvy submit` command
- added new `--compute` CLI argument
- `divvy write` can now be run without an outfile, which just prints the template to stdout.

### Changed
- Instead of passing extra variables as CLI args, you now must explicitly pass them to the `--compute` arg.
- The config file is now passed with a positional argument, instead of with `--config`.
- Made all one-char CLI args lowercase (`-P` to `-p`, `-S` to `-s`).
- Renamed default templates subfolder from submit_templates to divvy_templates
- removed `$PEPENV` from environment variables that may point to divvy computing configuration file. `$DIVCFG` is the only one now.

### Removed
- `config_file`, `no_env_error` and `no_compute_exception` from `ComputingConfiguration` class constructor

## [0.4.1] -- 2020-03-20
### Fixed
- `NameError` in `divvy init`; [#44](https://github.com/pepkit/divvy/issues/44)

### Added
- possibility to execute library module as a script: `python -m divvy ...`

### Changed
- improved error message when config format is incompatible

## [0.4.0] -- 2019-07-30
### Added
- Default templates for singularity and docker compute packages
- `divvy init` function now initializes a default config setup.

### Fixed
- `divvy` now shows help message with no args
- No longer print 'package activated' for default package

### Changed
- Restructured the objects to use more `yacman` functionality under the hood.

## [0.3.3] -- 2019-06-14
### Changed
- Removed utilities that are in `peppy`.
- Removed logging setup function.

## [0.3.2] -- 2019-05-09
### Changed
- Fixed `divvy list` command

## [0.3.1] -- 2019-04-24
### Changed
- Minor updates to improve interface with looper and peppy

## [0.3.0] -- 2019-04-19
### Changed
- Safer use of `yaml`
- Reduced verbosity for clearer usage
- The CLI now uses `divvy write` and `divvy list` subcommands

## [0.2.1] -- 2019-03-19
### Changed
- For environment variable population, use updated version of `attmap`

## [0.2.0] -- 2019-03-13
### Added
 - Implemented a `divvy` command-line interface
### Changed
- reduced verbosity

## [0.1.0] -- 2019-03-04
### Changed
- `divvy` looks for computing configuration file path in both `$DIVCFG` and `$PEPENV` environment variables and the former is given priority
- `ComputingConfiguration` class extends `AttMap` class, not `AttributeDict` 

