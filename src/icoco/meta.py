"""This module contains meta classes and functions to ensure ICoCo norm."""

from abc import ABC
import os
import pathlib
from types import FunctionType


from icoco.exception import WrongArgument, WrongContext
from icoco.utils import ICoCoMethodContext, ICoCoMethods

class Problem:  # pylint: disable=too-few-public-methods
    """Meta part of ICoCo problem implementation."""

    def __init__(self,
                 prob: str = None,
                 ensure_scope: bool = True,
                 working_directory: pathlib.Path = None
                 ) -> None:  # type: ignore
        """Constructor.

        Notes
        -----
            Internal set up and initialization of the code should not be done here,
            but rather in initialize() method.

        Parameters
        ----------
        prob : str, optional
            problem name, by default None.
        ensure_scope : bool, optional
            set True to ensure context when calling ICoCo methods, by default True.
        working_directory : pathlib.Path, optional
            defines the working directory when calling ICoCo methods, by default None.
        """
        super().__init__()

        self._problem_name: str = self.__class__.__name__ if prob is None else prob
        """Name of the problem"""

        self._ensure_scope = ensure_scope
        """Verification status."""
        self._initialized = False
        """Initialized status."""
        self._time_step_defined = False
        """Time step status."""
        self._working_directory: pathlib.Path = working_directory
        """Working directory when ICoCo method is called"""

    @property
    def problem_name(self) -> str:
        """Returns the problem name.

        Warning
        -------
            This is not part of ICoCo API.
        """
        return self._problem_name


def _decorator_icoco_methods(method):
    # pylint: disable=protected-access
    def check_initialized(self: 'Problem', *args, **kwargs):
        if self._ensure_scope and not self._initialized:
            raise WrongContext(prob=self.problem_name,
                               method=method.__name__,
                               precondition="called after initialize() or before terminate().")
        to_return = method(self, *args, **kwargs)
        if method.__name__ == 'terminate':
            self._initialized = False
        return to_return

    def check_not_initialized(self: 'Problem', *args, **kwargs):
        if self._ensure_scope and self._initialized:
            raise WrongContext(prob=self.problem_name,
                               method=method.__name__,
                               precondition="called before initialize() or after terminate().")
        to_return = method(self, *args, **kwargs)
        if method.__name__ == 'initialize':
            self._initialized = True
        return to_return
    if method.__name__ in ICoCoMethodContext.BEFORE_INITIALIZE:
        new_method = check_not_initialized
    elif method.__name__ in ['getMEDCouplingMajorVersion', 'isMEDCoupling64Bits',
                             'GetICoCoMajorVersion']:
        return method
    else:
        new_method = check_initialized

    new_method.__name__ = method.__name__
    new_method.__doc__ = method.__doc__
    new_method.__dict__.update(method.__dict__)
    return new_method


def _decorator_time_step_context(method):
    # pylint: disable=protected-access
    def check_inside_time_step(self: 'Problem', *args, **kwargs):
        if self._ensure_scope and not self._time_step_defined:
            raise WrongContext(prob=self.problem_name,
                               method=method.__name__,
                               precondition="called outside the TIME_STEP_DEFINED context."
                                            " (see Problem documentation)")
        to_return = method(self, *args, **kwargs)
        if method.__name__ in ['abortTimeStep', 'validateTimeStep']:
            self._time_step_defined = False
        return to_return

    def check_outside_time_step(self: 'Problem', *args, **kwargs):
        if self._ensure_scope and self._time_step_defined:
            raise WrongContext(prob=self.problem_name,
                               method=method.__name__,
                               precondition="called inside the TIME_STEP_DEFINED context."
                                            " (see Problem documentation)")
        to_return = method(self, *args, **kwargs)
        if method.__name__ == 'initTimeStep':
            self._time_step_defined = True
        return to_return
    if method.__name__ in ICoCoMethodContext.ONLY_INSIDE_TIME_STEP_DEFINED:
        new_method = check_inside_time_step
    elif method.__name__ in ICoCoMethodContext.ONLY_OUTSIDE_TIME_STEP_DEFINED:
        new_method = check_outside_time_step
    else:
        return method
    new_method.__name__ = method.__name__
    new_method.__doc__ = method.__doc__
    new_method.__dict__.update(method.__dict__)
    return new_method


def _decorator_check_attributes(method):
    # pylint: disable=protected-access
    def check_attributes(self: 'Problem', *args, **kwargs):
        to_return = method(self, *args, **kwargs)

        if not hasattr(self, 'problem_name'):
            setattr(self, 'problem_name', self.__class__.__name__)
        if not hasattr(self, '_ensure_scope'):
            setattr(self, '_ensure_scope', True)
        if not hasattr(self, '_initialized'):
            setattr(self, '_initialized', False)
        if not hasattr(self, '_time_step_defined'):
            setattr(self, '_time_step_defined', False)

        if not hasattr(self, '_working_directory'):
            setattr(self, '_working_directory', None)

        if (self._working_directory is not None and
                not pathlib.Path(self._working_directory).exists()):
            raise WrongArgument(prob=self.problem_name,
                                method="__init__",
                                arg="working_directory",
                                condition="invalid path is provided",
                                )

        return to_return

    new_method = check_attributes
    new_method.__name__ = method.__name__
    new_method.__doc__ = method.__doc__
    new_method.__dict__.update(method.__dict__)
    return new_method


def _decorator_working_dir(method):
    # pylint: disable=protected-access
    def in_working_dir(self: 'Problem', *args, **kwargs):

        origin = pathlib.Path().absolute()
        try:
            if self._working_directory:
                os.chdir(self._working_directory)
            to_return = method(self, *args, **kwargs)
        finally:
            if self._working_directory:
                os.chdir(origin)

        return to_return

    new_method = in_working_dir
    new_method.__name__ = method.__name__
    new_method.__doc__ = method.__doc__
    new_method.__dict__.update(method.__dict__)
    return new_method


class CheckScopeMeta(type):
    """! Metaclass related to the use of checkScope. """

    def __init__(cls, clsname, superclasses, attributedict):
        type.__init__(cls, clsname, superclasses, attributedict)

    def __new__(cls, clsname, superclasses, attributedict):

        new_dict = {}
        for attr_name, item in attributedict.items():
            if isinstance(item, FunctionType) and item.__name__ == '__init__':
                new_dict[attr_name] = _decorator_check_attributes(item)
            elif isinstance(item, FunctionType) and item.__name__ in ICoCoMethods.ALL:
                new_dict[attr_name] = _decorator_working_dir(item)
                new_dict[attr_name] = _decorator_time_step_context(new_dict[attr_name])
                new_dict[attr_name] = _decorator_icoco_methods(new_dict[attr_name])
            else:
                new_dict[attr_name] = item
        newclass = type.__new__(cls, clsname, superclasses, new_dict)
        if '__doc__' in attributedict:
            newclass.__doc__ = attributedict['__doc__']
        else:
            for surperclass in superclasses:
                if hasattr(surperclass.__dict__, '__doc__'):
                    newclass.__doc__ = surperclass.__dict__['__doc__']
                    return newclass
        return newclass


class MetaProblem(type(ABC), CheckScopeMeta):
    """Meta class for Problem."""
