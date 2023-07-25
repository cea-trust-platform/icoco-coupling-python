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

import pathlib as _pathlib

__version__ = (_pathlib.Path(__file__).parent.resolve() / "VERSION").read_text(
    encoding="utf-8").strip()

__copyright__ = '2023, CEA'
__author__ = 'CEA'

from .utils import (ICOCO_VERSION, ICOCO_MAJOR_VERSION, ICOCO_MINOR_VERSION,  # noqa: F401
                    ValueType, medcoupling)  # noqa: F401

from .exception import WrongContext, WrongArgument, NotImplementedMethod  # noqa: F401

from .problem_server import ProblemClient, ServerManager  # noqa: F401
from .problem_wrapper import ProblemWrapper  # noqa: F401
from .problem import Problem  # noqa: F401
