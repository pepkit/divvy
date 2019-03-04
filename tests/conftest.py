import os
import glob
import divvy
import pytest


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, 'data/pepenv-master')
FILES = glob.glob(DATA_DIR + "/*.yaml")
DCC_ATTRIBUTES = divvy.ComputingConfiguration().keys()


@pytest.fixture
def empty_dcc():
    """ Provide the empty/default ComputingConfiguration object """
    return divvy.ComputingConfiguration()


@pytest.fixture(params=FILES)
def dcc(request):
    """ Provide ComputingConfiguration objects for all files in pepenv repository """
    return divvy.ComputingConfiguration(request.param)





