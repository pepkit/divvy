#!/usr/bin/env bash
# This script can be used to update the data for the unit tests
rm -rf pepenv-master
wget https://github.com/pepkit/pepenv/archive/master.zip
unzip master.zip
rm master.zip