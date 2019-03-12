# Changelog

## divvy [0.2] - Unreleased

### Added
 - Implemented a `divvy` command-line interface

### Changed
- reduced verbosity

## divvy [0.1] - 2019-03-04

### Changed
- `divvy` looks for computing configuration file path in both `$DIVCFG` and `$PEPENV` environment variables and the former is given priority
- `ComputingConfiguration` class extends `AttMap` class, not `AttributeDict` 

