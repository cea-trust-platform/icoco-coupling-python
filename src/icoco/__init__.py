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

from .utils import ICOCO_VERSION, ICOCO_MAJOR_VERSION, ICOCO_MINOR_VERSION, ValueType, medcoupling

from .exception import WrongContext, WrongArgument, NotImplementedMethod

from .problem_wrapper import ProblemWrapper
from .problem import Problem
