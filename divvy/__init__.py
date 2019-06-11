"""Project configuration, particularly for logging.

Project-scope constants may reside here, but more importantly, some setup here
will provide a logging infrastructure for all of the project's modules.
Individual modules and classes may provide separate configuration on a more
local level, but this will at least provide a foundation.

"""

import logging
from ._version import __version__
from .compute import ComputingConfiguration
from .const import *
from .utils import write_submit_script

__classes__ = ["ComputingConfiguration"]
__all__ = __classes__ + [write_submit_script.__name__]

# Ensure that we have a handler and don't get a logging exception.
# Note that this was originally with looper.models.
_LOGGER = logging.getLogger(__name__)
if not logging.getLogger().handlers:
    _LOGGER.addHandler(logging.NullHandler())
