# Changelog

## Unreleased

## divvy [0.3.1] - 2019-04-24
### Changed
- Minor updates to improve interface with looper and peppy



## divvy [0.3] - 2019-04-19
### Changed
- Safer use of `yaml`
- Reduced verbosity for clearer usage
- The CLI now uses `divvy write` and `divvy list` subcommands

## divvy [0.2.1] - 2019-03-19
### Changed
- For environment variable population, use updated version of `attmap`

## divvy [0.2] - 2019-03-13
### Added
 - Implemented a `divvy` command-line interface
### Changed
- reduced verbosity

## divvy [0.1] - 2019-03-04
### Changed
- `divvy` looks for computing configuration file path in both `$DIVCFG` and `$PEPENV` environment variables and the former is given priority
- `ComputingConfiguration` class extends `AttMap` class, not `AttributeDict` 

