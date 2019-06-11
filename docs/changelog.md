# Changelog

## [0.3.3] -- 2019-06-11
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

