"""
ICoCo file common to several codes
Version 2 -- 02/2021

WARNING: this file is part of the official ICoCo API and should not be modified.
The official version can be found at the following URL:

https://github.com/cea-trust-platform/icoco-coupling

The package ICoCo (Interface for code coupling) encompasses all the classes
and methods needed for the coupling of codes.
See :class:`icoco.problem.Problem` to start with.

"""

__copyright__ = '2023, CEA'
__author__ = 'CEA'

from .exception import WrongContext, WrongArgument, NotImplementedMethod  # noqa: F401
from .problem import (Problem, ValueType,  # noqa: F401
                      ICOCO_VERSION, ICOCO_MAJOR_VERSION, ICOCO_MINOR_VERSION)  # noqa: F401
from .version import get_version  # noqa: F401

__version__ = get_version()
